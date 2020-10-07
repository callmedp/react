

const gigetNonConsBinStringCount = (number) =>{

    if(number <= 0) return 0;

    let firstNumber =1, secondNumber = 1, thirdNumber;

    for(let i = 1; i <= number; i++){
        thirdNumber = firstNumber + secondNumber
        firstNumber = secondNumber
        secondNumber = thirdNumber
    }
    return thirdNumber
}

console.log(getNonConsBinStringCount(5))