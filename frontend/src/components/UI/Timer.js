import React from "react";
import classes from "./Timer.module.css";
import { useStopwatch } from "react-timer-hook";

const Timer = () => {
  const { seconds, minutes, hours, days } = useStopwatch({ autoStart: true });

  return (
    <div className={classes.timer}>
      {days !== 0 && <span>{days}day </span>}
      {hours !== 0 && <span>{hours}hr </span>}
      {minutes !== 0 && <span>{minutes}min </span>}
      {seconds !== 0 && <span>{seconds}sec</span>}
    </div>
  );
};

export default Timer;
 