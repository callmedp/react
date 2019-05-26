#python imports
import json

#django imports

#local imports
from .models import OrderCustomisation

#inter app imports

#third party imports

#Global Constants
MIN_DEPTH = 2 # Assuming Personal and Summary always come on top
MAX_DEPTH = 10 # Max entities catered by Builder till date

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

    def __init__(self,**kwargs):
        self.candidate_id = kwargs.get('candidate_id')
        self.template_no = kwargs.get('template_no')
        self.saved_entity_data = []
        self.current_entity_obj = OrderCustomisation.objects.filter(\
            candidate__candidate_id=self.candidate_id,template_no=self.template_no).first()
        
        if self.current_entity_obj:
            self.saved_entity_data = json.loads(self.current_entity_obj.entity_position)

    def get_pos_item_mapping(self):
        return {d['pos']:d for d in self.saved_entity_data}

    def get_saved_entity_data():
         return self.saved_entity_data

    def get_entity_pos(self,entity_id):
        entity_status = {}
        for item in self.saved_entity_data:
            if item.get('entity_id') == entity_id:
                entity_status = item
                break

        entity_pos = entity_status.get('pos',-1)
        return entity_pos

    def get_entity_alignment(self,entity_id):
        entity_status = {}
        for item in self.saved_entity_data:
            if item.get('entity_id') == entity_id:
                entity_status = item
                break

        entity_alignment = entity_status.get('alignment',"center")
        return entity_alignment

    def _handle_center_item_swapping(self,pos,step):
        pos_item_mapping = self.get_pos_item_mapping()
        step_item = pos_item_mapping.get(pos+step)
        
        if step_item.get('alignment') in ['left','right']:
            return {pos+step:pos,
                    pos+(2*step):pos+step,
                    pos:pos+(2*step)
                    }

        return {pos+step:pos,pos:pos+step}

    def get_swap_dict_for_entity(self,entity_pos,alignment,step):
        end = MIN_DEPTH if step == -1 else MAX_DEPTH + 1
        swap_dict = {}
        pos_item_mapping = self.get_pos_item_mapping()

        if alignment == "center":
            if entity_pos + step > MAX_DEPTH or entity_pos + step <= MIN_DEPTH:
                return swap_dict

            swap_dict.update(self._handle_center_item_swapping(entity_pos,step))
            return swap_dict

        for pos in range(entity_pos+step,end,step):
            pos_item =  pos_item_mapping.get(pos)
            
            if not pos_item:
                continue

            if pos_item['alignment'] == alignment:
                swap_dict.update({pos:entity_pos,entity_pos:pos})
                break

        return swap_dict

    def get_item_data_with_swapped_position(self,item,swap_dict):
        current_pos = item.get('pos')
        data_copy = {key:value for key,value in item.items()}
        swap_positions = [x for x in swap_dict.keys()]

        if current_pos not in swap_positions:
            return data_copy

        data_copy['pos'] = swap_dict[current_pos]
        return data_copy

    def move_entity(self,entity_id,step):
        entity_pos = self.get_entity_pos(entity_id)
        entity_alignment = self.get_entity_alignment(entity_id)
        swap_dict = self.get_swap_dict_for_entity(
            entity_pos,entity_alignment,step)

        if not swap_dict:
            return self.saved_entity_data

        swapped_entity_data = [self.get_item_data_with_swapped_position(x,swap_dict) \
                                    for x in self.saved_entity_data]
        return sorted(swapped_entity_data,key=lambda x:x['pos'])

