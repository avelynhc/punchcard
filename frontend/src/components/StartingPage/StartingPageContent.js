import { Fragment, useState, useContext } from "react";
import classes from "./StartingPageContent.module.css";

import AddTask from "../TimeTracking/AddTask";
import Timer from "../UI/Timer";
import AuthContext from "../../store/auth-context";

const BACKEND_API = "http://127.0.0.1:4000";

const StartingPageContent = () => {
  const [isAdded, setIsAdded] = useState(false);
  const authCtx = useContext(AuthContext);

  const addTaskHandler = (newTask) => {
    const token = localStorage.getItem("token");
    fetch(`${BACKEND_API}/task/${newTask}`, {
      method: "POST",
      body: JSON.stringify(newTask),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
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
      .then((data) => {
        authCtx.token(data.access_token);
      })
      .catch((err) => {
        console.log(err);
        alert(err.message);
      });
  };

  return (
    <Fragment>
      <section className={classes.starting}>
        <h1>Welcome to punch card!</h1>
        <img
          src="https://static.righto.com/images/1401-boot/card-codes-w600.jpg"
          alt="punch-card"
        ></img>
      </section>
      <section>
        <AddTask onAddTask={addTaskHandler}></AddTask>
        {isAdded && <Timer />}
      </section>
    </Fragment>
  );
};

export default StartingPageContent;


