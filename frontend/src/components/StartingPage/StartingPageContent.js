import classes from "./StartingPageContent.module.css";
import { Link } from 'react-router-dom';

const StartingPageContent = () => {

  return (
    <>
      <section className={classes.starting}>
        <h1>Welcome to punch card!</h1>
        <br />
        <br />
        <Link className={classes.link} to="/new">Create a new task</Link>
      </section>
    </>
  );
};

export default StartingPageContent;
