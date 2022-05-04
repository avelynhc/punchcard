import { useContext, useEffect } from "react";
import { Switch, Route, Redirect, useHistory } from "react-router-dom";
import Layout from "./components/Layout/Layout";
import UserProfile from "./components/Profile/UserProfile";
import AuthPage from "./pages/AuthPage";
import HomePage from "./pages/HomePage";
import AuthContext from "./store/auth-context";

const BACKEND_API = "http://127.0.0.1:4000";

const App = () => {
  const authCtx = useContext(AuthContext);
  const isLoggedIn = authCtx.isLoggedIn;
  const history = useHistory();

  useEffect(() => {
    let token = localStorage.getItem("token");
    if (token) {
      fetch(`${BACKEND_API}/me`, {
        headers: {
          Authorization: "Bearer " + token,
        },
      })
        // .then((res) => {
        //   console.log(res)
        //   return res.json();
        // })
        .then((data) => {
          if (data.me) {
            authCtx.isLoggedIn(true);
            history.push('/');
          }
        })
        .catch((err) => {
          console.log(err);
          localStorage.removeItem("token");
        });
    } else {
      history.push('/auth');
    }
  }, [isLoggedIn]);

  return (
    <Layout>
      <Switch>
          <Route path="/" exact>
            <HomePage />
          </Route>
        )
          <Route path="/auth" exact>
            <AuthPage />
          </Route>
        )
        <Route path="/profile" exact>
          <UserProfile />
        </Route>
        <Route path="*">
          <Redirect to="/" />
        </Route>
      </Switch>
    </Layout>
  );
};

export default App;
