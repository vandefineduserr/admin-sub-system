import { EditorState } from "draft-js";
import Authorization from "./authorisation";
import axios from "axios";

class Project {
    getProjectInfo(ws_name: string, project_id: string) {
        return axios.get(`/api/project/${ws_name}/${project_id}`, Authorization.getAxiosConfig())
    }

    getProjectDescription(ws_name: string, project_id: string) {
        return axios.get(`/api/project/${ws_name}/${project_id}/description/`, Authorization.getAxiosConfig())
    }

    setProjectDescription(ws_name: string, project_id: string, data: any) {
        return axios.post(`/api/project/${ws_name}/${project_id}/description/`, data, Authorization.getAxiosConfig())
    }

    createProject(ws_name: string, project: any) {
        return axios.post(`/api/project/${ws_name}/create`, project,  Authorization.getAxiosConfig())
    }

    deleteProject(ws_name: string, project_id: string) {
        return axios.delete(`/api/project/${ws_name}/${project_id}`, Authorization.getAxiosConfig())
    }

    checkTaskStatus(ws_name: string, project_id: string){
        return axios.get(`/api/project/${ws_name}/${project_id}/tasks/check`, Authorization.getAxiosConfig())
    }
}

const project = new Project

export default project