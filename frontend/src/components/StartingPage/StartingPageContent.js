import { useState } from "react";
import classes from "./StartingPageContent.module.css";

import AddTask from "../TimeTracking/AddTask";
import Timer from "../UI/Timer";

const BACKEND_API = "http://127.0.0.1:4000";
const StartingPageContent = () => {
  const [isAdded, setIsAdded] = useState(false);

  const addTaskHandler = (newTask) => {
    const url = isAdded
      ? `${BACKEND_API}/task/${newTask}/finish`
      : `${BACKEND_API}/task/${newTask}`;

    const token = localStorage.getItem("token");
    // TODO: make the check for token happen in a single place
    fetch(url, {
      method: "POST",
      body: JSON.stringify(newTask),
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    })
      .then((res) => {
        if (res.ok) {
          setIsAdded(true);
          return res.json();
        } else {
          throw new Error("failed to add a new task");
        }
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  return (
    <>
      <section className={classes.starting}>
        <h1>Welcome to punch card!</h1>
      </section>
      <section>
        <AddTask onAddTask={addTaskHandler} />
        {isAdded && <Timer />}
      </section>
    </>
  );
};

export default StartingPageContent;
