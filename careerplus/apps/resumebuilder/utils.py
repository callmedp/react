# python imports
import os, json, logging
from io import BytesIO

# django imports
from django.conf import settings
from django.template.loader import get_template

# local imports
from .tasks import generate_and_upload_resume_pdf
from .models import OrderCustomisation, Candidate
from .constants import TEMPLATE_ALLOW_LEFT_RIGHT_SWITCH

# inter app imports
from core.library.gcloud.custom_cloud_storage import GCPResumeBuilderStorage

# third party imports
import pdfkit
import zipfile
from PIL import Image
from celery import group

# Global Constants
MIN_DEPTH = 2  # Assuming Personal and Summary always come on top
MAX_DEPTH = 11  # Max entities catered by Builder till date


class ResumeEntityReorderUtility:
    """
    Current pos - left 
        Swap with first top left if step  == -1
        Swap with first bottom left if step  == -1

    Current pos - right 
        Swap with first top right if step  == -1
        Swap with first bottom right if step  == -1
    
    Current pos - center
        Swap if top/bottom blocks also center
        Else move both left & right sections up/down depending upon step value.
    """

    def __init__(self, **kwargs):
        self.candidate_id = kwargs.get('candidate_id')
        self.template_no = kwargs.get('template_no')
        self.saved_entity_data = []
        self.current_entity_obj = OrderCustomisation.objects.filter( \
            candidate__candidate_id=self.candidate_id, template_no=self.template_no).first()

        if self.current_entity_obj:
            self.saved_entity_data = json.loads(self.current_entity_obj.entity_position)

    def get_pos_item_mapping(self):
        return {d['pos']: d for d in self.saved_entity_data}

    def get_saved_entity_data():
        return self.saved_entity_data

    def get_entity_pos(self, entity_id):
        entity_status = {}
        for item in self.saved_entity_data:
            if item.get('entity_id') == entity_id:
                entity_status = item
                break

        entity_pos = entity_status.get('pos', -1)
        return entity_pos

    def get_entity_alignment(self, entity_id):
        entity_status = {}
        for item in self.saved_entity_data:
            if item.get('entity_id') == entity_id:
                entity_status = item
                break

        entity_alignment = entity_status.get('alignment', "center")
        return entity_alignment

    def swap_entities_for_deactivation(self, entity_pos, alignment):
        pos_in_focus = entity_pos
        end = MAX_DEPTH + 1
        swap_dict = {}
        pos_item_mapping = self.get_pos_item_mapping()

        for pos in range(entity_pos + 1, end):
            pos_item = pos_item_mapping.get(pos)

            if not pos_item:
                continue

            if pos_item['alignment'] == alignment and pos_item['active']:
                swap_dict.update({pos_in_focus: [pos, alignment, entity_pos != pos_in_focus]})
                pos_in_focus = pos
                break

        swap_dict.update({pos_in_focus: [entity_pos, alignment, True]})
        return swap_dict

    def _handle_center_item_swapping(self, pos, step):
        if step == 0:
            return self.swap_entities_for_deactivation(pos, "center")

        pos_item_mapping = self.get_pos_item_mapping()
        step_item = pos_item_mapping.get(pos + step)
        if not step_item.get('active'):
            return {}

        if step_item.get('alignment') in ['left', 'right']:
            return {pos + step: [pos, pos_item_mapping[pos + step].get('alignment'), True],
                    pos + (2 * step): [pos + step, pos_item_mapping[pos + (2 * step)].get('alignment'), True],
                    pos: [pos + (2 * step), pos_item_mapping[pos].get('alignment'), True]
                    }

        return {pos + step: [pos, "center", True], pos: [pos + step, "center", True]}

    def get_swap_dict_for_entity(self, entity_pos, alignment, step):
        end = MIN_DEPTH if step == -1 else MAX_DEPTH + 1
        swap_dict = {}
        pos_item_mapping = self.get_pos_item_mapping()

        if alignment == "center":
            if entity_pos + step > MAX_DEPTH or entity_pos + step <= MIN_DEPTH:
                return swap_dict

            swap_dict.update(self._handle_center_item_swapping(entity_pos, step))
            return swap_dict

        if step == 0:
            return self.swap_entities_for_deactivation(entity_pos, alignment)

        for pos in range(entity_pos + step, end, step):
            pos_item = pos_item_mapping.get(pos)

            if not pos_item:
                continue

            if pos > MAX_DEPTH or pos <= MIN_DEPTH:
                return swap_dict

            allow_switch = (TEMPLATE_ALLOW_LEFT_RIGHT_SWITCH.get(self.template_no) or \
                            pos_item['alignment'] == alignment) and pos_item['alignment'] != 'center'

            if allow_switch and pos_item['active']:
                swap_dict.update({pos: [entity_pos, alignment, True], entity_pos: [pos, alignment, True]})
                break

        return swap_dict

    def get_item_data_with_swapped_position(self, item, swap_dict):
        current_pos = item.get('pos')
        data_copy = {key: value for key, value in item.items()}
        swap_positions = [x for x in swap_dict.keys()]

        if current_pos not in swap_positions:
            return data_copy

        data_copy['pos'] = swap_dict[current_pos][0]
        data_copy['alignment'] = swap_dict[current_pos][1]
        data_copy['active'] = swap_dict[current_pos][2]
        return data_copy

    def move_entity(self, entity_id, step):
        entity_pos = self.get_entity_pos(entity_id)
        entity_alignment = self.get_entity_alignment(entity_id)
        swap_dict = self.get_swap_dict_for_entity(
            entity_pos, entity_alignment, step)

        if not swap_dict:
            return self.saved_entity_data

        swapped_entity_data = [self.get_item_data_with_swapped_position(x, swap_dict) \
                               for x in self.saved_entity_data]
        return sorted(swapped_entity_data, key=lambda x: x['pos'])


class ResumeGenerator(object):

    def save_order_resume_pdf(self, order=None, is_combo=False, index=None):

        if not order:
            return None, None

        data_to_send = {"order_id": order.id, "template_no": index}



        if not is_combo:
            data_to_send.update({"send_mail": True})
            generate_and_upload_resume_pdf.delay(json.dumps(data_to_send))
            return

        for i in range(1, 6):
            data_to_send.update({"template_no": i})
            generate_and_upload_resume_pdf.delay(json.dumps(data_to_send))


# Uplod byte stream to cloud
def store_resume_file(file_dir, file_name, file_content):
    directory_path = "{}/{}".format(settings.RESUME_TEMPLATE_DIR, file_dir)
    if settings.IS_GCP:
        gcp_file = GCPResumeBuilderStorage().open("{}/{}".format(directory_path, file_name), 'wb')
        gcp_file.write(file_content)
        gcp_file.close()
        return

    directory_path = "{}/{}".format(settings.MEDIA_ROOT, directory_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    dest = open("{}/{}".format(directory_path, file_name), 'wb')
    dest.write(file_content)
    dest.close()
