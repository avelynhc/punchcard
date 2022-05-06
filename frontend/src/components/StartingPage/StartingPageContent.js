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
    let url;
    isAdded
      ? (url = `${BACKEND_API}/task/${newTask}`)
      : (url = `${BACKEND_API}/task/${newTask}/finish`);

    const token = localStorage.getItem("token");
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
      .then((data) => {
        console.log(data);
        // authCtx.token(data.access_token);
        authCtx.token = token;
      })
      .catch((err) => {
        console.log(err.message);
        alert(err.message);
      });
  };

  return (
    <Fragment>
      <section className={classes.starting}>
        <h1>Welcome to punch card!</h1>
      </section>
      <section>
        <AddTask onAddTask={addTaskHandler}></AddTask>
        {isAdded && <Timer />}
      </section>
    </Fragment>
  );
};

export default StartingPageContent;
