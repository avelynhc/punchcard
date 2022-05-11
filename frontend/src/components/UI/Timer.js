import React from "react";
import { useStopwatch } from "react-timer-hook";

const Timer = () => {
  const { seconds, minutes, hours, days } =
    useStopwatch({ autoStart: true });

  // TODO: replace inline styles with proper styles
  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ fontSize: "100px" }}>
        <span>{days}</span>:<span>{hours}</span>:<span>{minutes}</span>:
        <span>{seconds}</span>
      </div>
    </div>
  );
};

export default Timer;
