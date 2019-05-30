import {scroller} from "react-scroll/modules";


export const scrollOnErrors = (errors,type,offset) =>{
    console.log(errors)
    const {list} = errors
    let pos;

    error_pos:
    for(let i in list){
        for(let j in list[i]){
            if(list[i][j]){
                pos =i;
                break error_pos;
            } 
        }
    }
    console.log(pos)

    scroller.scrollTo(`${type}${pos}`, {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuad',
        offset,
    })
}