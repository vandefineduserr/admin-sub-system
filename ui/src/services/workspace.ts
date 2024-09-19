import Authorization from "./authorisation";
import axios from "axios";

class Workspace {

    getWorkspaceInfo(ws_name: string){
        return axios.get(`/api/workspace/${ws_name}`,  Authorization.getAxiosConfig())
    }

    createWorkspace(form: any) {
        return axios.post(`/api/workspace/create`, form, Authorization.getAxiosConfig())
    }


}

const workspace = new Workspace

export default workspace