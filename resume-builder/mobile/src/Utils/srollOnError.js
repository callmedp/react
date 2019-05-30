import {scroller} from "react-scroll/modules";


export const scrollOnErrors = (errors,type,offset) =>{
    let id,pos
    if(type === 'profile'){
        for(let key in errors){
            if(errors[key]) id =key
        }

    }
    else{
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
    }
    console.log(id)
    scroller.scrollTo(`${id}`, {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuad',
        offset,
    })
}