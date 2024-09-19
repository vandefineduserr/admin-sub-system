export interface AccessToken {
  role?: string;
  sub?: string;
  user_id?: string;
  iat?: number;
  exp?: number;
}

export interface PickerProps {
  cat: any;
  catType: any;
}

export interface Me {
  uid: string
  firstname: string;
  lastname: string;
  photo?: string;
  email: string;
  password?: string;
  workspaces: string[]
}



// new interfaces
export interface Workspace {
  uid: string;
  name: string;
  type: number;
  members: Member[];
  invitations?: Invited[];
  projects?: string[];
  projectsDetails?: Project[];
  tasks?: String[]
}

export interface Member extends Me {
  role: number;
}

export interface Invited {
  email: string;
  role: number;
}

export interface Project {
  uid: string;
  name: string;
  layout: string;
  description?: any;
  creationDate: string;
  expiredDate?: string;
  cvs?: string[];
  searchParams?: SearchParams
  parsingJobs?: string[];
  aiJobs?: string[];
  stat?: ProjectStat;
}

export interface ProjectStat {
  aiRanking?: string;
  payments?: number;
  budget?: number;
}

export interface SearchParams {
  age_min: number;
  age_max: number;
  sex: string;
  region: string
  in_region: boolean
  profession: string
  min_salary: string
  max_salary: string
  employment: string
  work_schedule: string
  education: string
  in_service: string
  citizenship: string
  work_permit: string
  languages?: string[]
  car_category: string
  car: boolean
  skills?: string[]
  key_words?: string[]
}

export interface Task {
  id: String;
  status: String;
  project: String;
  result: any;
}
