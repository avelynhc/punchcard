import classes from "./StartingPageContent.module.css";
import { Link } from 'react-router-dom';

const StartingPageContent = () => {

  return (
    <>
      <section className={classes.starting}>
        <h1>Free Time Tracking App</h1>
        <h3>Punch card is the time tracking app for tracking the amount of time you spend on projects, tasks, and various activities.</h3>
        <br />
        <br />
        <Link className={classes.link} to="/new">Create a new task</Link>
      </section>
    </>
  );
};

export default StartingPageContent;
