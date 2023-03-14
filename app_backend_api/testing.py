import "./styles.css";
import { IKContext, IKUpload } from "imagekitio-react";

export default function App() {
  const onSuccess = (success) => {
    console.log("success");
    console.log(success);

    console.log(success.url);
  };

  // ^^ gets a responce on url + data when upload complete
  const onError = (error) => {
    console.log("error");
    console.log(error);
  };

  // private_Wdi3LTfI9KmRws+U/NZDkQxSdTE=
  // https://ik.imagekit.io/allnations/
  // you need the publxc?

  // public_aDahP208/A6D0rqkxn5opFd4m6o=
  // nice!
  // qhat did tou  do?
  //okay sooooo its goina be odd lol
  //the IKContext has to Authenticate with your Backend API. like your own API.
  //i used a app to open a portal from my local  host to the app and created a route that auths it .
  //the responace gives a token and sifnature and expire which then gets sent to the IKcontext

  //

  //so for you.. create a view

  // in that view pip install  ImageKit

  //  from imagekitio import ImageKit

  // in the view  can be a get request
  //  add this  ->>> imagekit = ImageKit(
  // public_key='public_aDahP208/A6D0rqkxn5opFd4m6o=',
  // private_key='private_Wdi3LTfI9KmRws+U/NZDkQxSdTE=',
  // url_endpoint = 'the url for ur back end (localhost....)' )

  //new var
  //  auth_params = imagekit.get_authentication_parameters()

  // then return auth_params

  // the url for that view goes into  authenticationEndpoint
  // okay so it would be appName.heroku.com/viewUrl <<< ? for prod yes. for testing it would be ur localhost
  // how can i setup localhost to access www? i would need ngrok? .. no i just needed that for this sandbox
  //for you can can just tell it to route to localhost/9000 or w.e port it is  / the rest of teh url to that view
  // got it. okay

  // this is what it would look like for a node back end

  // router.get('/loveAndFaith', async (req, res) => {

  //   const imageKit = new ImageKit({
  //     publicKey: 'public_aDahP208/A6D0rqkxn5opFd4m6o=',
  //     privateKey: 'private_Wdi3LTfI9KmRws+U/NZDkQxSdTE=',
  //     urlEndpoint: 'https://ik.imagekit.io/allnations/',
  //   });

  //   const authenticationParameters = imageKit.getAuthenticationParameters();
  //   res.json(authenticationParameters);
  // });

//got it ?
// makes perfect sence. i will go ahead and apply this. 
// thank you again for saving me for the 100th time
// no worries man ! its all easy work we all learn lol
// ill ping you when successful
// for sure !
// let me copy and paste first. i think if you stop session, i will lose code
  return (
    <div className="App">
      <IKContext
        publicKey="public_aDahP208/A6D0rqkxn5opFd4m6o="
        urlEndpoint="https://ik.imagekit.io/allnations/"
        authenticationEndpoint={" url to ur test server or prod server"}
      >
        <IKUpload onError={onError} onSuccess={onSuccess} />
      </IKContext>
    </div>
  );
}
