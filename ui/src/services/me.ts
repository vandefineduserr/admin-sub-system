import Authorization from "./authorisation";
import axios from "axios";

class MyProfile {
    getMyInfo(){
        return axios.get(`/api/me/info`, Authorization.getAxiosConfig())
    }
}

const myProfile = new MyProfile

export default myProfile