import {scroller} from "react-scroll/modules";


export const scrollOnErrors = (errors,type,offset) =>{
    let id,pos
    const {list} = errors
    
    error_pos:
    for(let i in list){
        for(let j in list[i]){
            if(list[i][j]){
                pos =i;
                break error_pos;
            } 
        }
    }
    id =`${type}${pos}`
    scroller.scrollTo(`${id}`, {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuad',
        offset,
        containerId:type
    })
}