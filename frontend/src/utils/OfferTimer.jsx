import React, {useRef, useState, useEffect} from 'react';

const OfferTimer = (props) => {
  const {timerDate, cssClass, type} = props;
  const [timerDays, setTimerDays] = useState('00');
  const [timerHours, setTimerHours] = useState('00');
  const [timerMinutes, setTimerMinutes] = useState('00');
  const [timerSeconds, setTimerSeconds] = useState('00');
  let interval = useRef();
  
  const startTimer = (countdownDate) => {
    const now = new Date().getTime();
    const distance = countdownDate - now;
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    if (distance < 0) clearInterval(interval.current);
    else {
      setTimerDays(days);
      setTimerHours(hours);
      setTimerMinutes(minutes);
      setTimerSeconds(seconds);
    }

    // console.log(timerDays, timerHours, timerMinutes, timerSeconds)
  };
  
  const saveInLocalStorage = (time) => {
    localStorage.setItem("timer", time);
  }
  
  const getTimeFromLocalStorage = () => {
    return localStorage.getItem("timer");
  }
  
  useEffect(() => {
    const localTimer = getTimeFromLocalStorage();
    
    if (localTimer) {
      interval.current = setInterval(() => {
        startTimer(+localTimer);
      }, 500);
    }
    else {
      const countdownDate = new Date(timerDate).getTime();

      saveInLocalStorage(countdownDate);
      interval.current = setInterval(() => {
        startTimer(+countdownDate);
      }, 500);
    }
    
    return () => clearInterval(interval.current);
  });
    
  return (
    <>
      <span className={cssClass}>
        <strong>{timerDays}</strong> 
        {type === 'main' ? <em>D</em> : <em>Days</em>}
      </span>
      <span className={cssClass}>
        <strong>{timerHours}</strong> 
        {type === 'main' ? <em>H</em> : <em>Hours</em>}
      </span>
      <span className={cssClass}>
        <strong>{timerMinutes}</strong> 
        {type === 'main' ? <em>M</em> : <em>Min.</em>}
      </span>
      <span className={cssClass}>
        <strong>{timerSeconds}</strong> 
        {type === 'main' ? <em>S</em> : <em>Sec.</em>}
      </span>
    </>
  )
}
  
export default OfferTimer;