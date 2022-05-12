import { useContext, useEffect } from "react";
import { Switch, Route, Redirect, useHistory } from "react-router-dom";
import Layout from "./components/Layout/Layout";
import UserProfile from "./components/Profile/UserProfile";
import AuthPage from "./pages/AuthPage";
import HomePage from "./pages/HomePage";
import AuthContext from "./store/auth-context";
import TaskDetailPage from "./pages/TaskDetailPage";

const BACKEND_API = "http://127.0.0.1:4000";

const App = () => {
  const authCtx = useContext(AuthContext);
  const history = useHistory();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${BACKEND_API}/me`, {
        headers: {
          Authorization: "Bearer " + token,
        },
      })
        .then((data) => {
          if (data.ok) {
            return data.json();
          } else {
            throw new Error("failed to get me information");
          }
        })
        .then((resp) => {
          if (resp.me) {
            history.push("/");
          }
        })
        .catch((err) => {
          console.log(err);
          localStorage.removeItem("token");
        });
    } else {
      history.push("/auth");
    }
  }, [authCtx, history]);

  return (
    <Layout>
      <Switch>
        <Route path="/" exact>
          <HomePage />
        </Route>
        <Route path="/auth" exact>
          <AuthPage />
        </Route>
        <Route path="/task" exact>
          <UserProfile />
        </Route>
        <Route path="/task/:taskName" exact>
          <TaskDetailPage />
        </Route>
        <Route path="*">
          <Redirect to="/" />
        </Route>
      </Switch>
    </Layout>
  );
};

export default App;
