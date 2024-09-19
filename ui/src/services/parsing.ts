import Authorization from "./authorisation";
import axios from "axios";

class Parsing {
  checkParsersAvailability() {
    return axios.get(`/parse/ping`, Authorization.getAxiosConfig());
  }

  findCandidates(data: any, ws_name: string, project: string) {
    return axios.post(
      `/parse/find`,
      { search_params: data, ws_name: ws_name, project: project },
      Authorization.getAxiosConfig()
    );
  }
}

const parsing = new Parsing();

export default parsing;
