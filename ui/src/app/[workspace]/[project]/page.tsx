"use client";
//system
import { useEffect, useState } from "react";

//components
import LayoutPicker from '@/app/components/project/LayoutPicker';
import OfferConstructor from '@/app/components/project/OfferConstructor';
import ResumesByForm from '@/app/components/project/ResumesByForm';

//styles
import styles from "./page.module.sass";
import ProjectSettings from "@/app/components/project/ProjectSettings";
import project from "@/services/projects";
import LoadingScreen from "@/app/components/loading/loadingScreen";



export default function FormPage({
  params
} : {
  params: {workspace: string, project: string}
}) {
  const [catType, setCatType] = useState(0);
  const cat = (type: number) => setCatType(type);
  
  const [taskStatus, setTaskStatus] = useState("");
  const [forms, setForms] = useState([]);

  const [isLoading, setIsLoading] = useState(false);

  const getForms = async() => {
    const res = await project.checkTaskStatus(params.workspace, params.project)
    if (res.status === 200) {
      setForms((JSON.parse(res.data)).result)
      setTaskStatus("completed")
    }
  }

  useEffect(() => {
    const check = setInterval(() => {
      if (taskStatus === "completed") clearInterval(check)
      getForms();
    }, 20000)
    return () => clearInterval(check);
  })

  return (
    <main className={styles.main}>
      <div className={`${styles.container} ${styles.noScroll}`}>
        {isLoading == true && <LoadingScreen/>}
        <LayoutPicker cat={cat} catType={catType} />
        { catType == 0 ? <OfferConstructor ws={params.workspace} projectID={params.project}/> :
            catType == 1 ? <ResumesByForm forms={forms} workspaceName={params.workspace} projectName={params.project} /> : 
              <ProjectSettings ws={params.workspace} projectID={params.project}/> 
        }

      </div>
    </main>
  );
}
