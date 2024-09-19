import Authorization from "./authorisation";
import axios from "axios";

class AI {
  rateCandidate(data: any) {
    return axios.post(`/ai/get_percent`, data, Authorization.getAxiosConfig());
  }
}

const ai = new AI();

export default ai;
