//system
import dynamic from "next/dynamic";
import React, { useEffect, useState } from "react";

//services
// import ParamsOffer from '@/services/paramsOffer';

//components
import Success from '@/app/components/notfications/success';
import Error from '@/app/components/notfications/error';
import LoadingScreen from "@/app/components/loading/loadingScreen";

//styles
import styles from '@/app/[workspace]/[project]/page.module.sass';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
//editor
import { EditorState } from "draft-js";
import { convertToHTML } from "draft-convert";
import project from "@/services/projects";
const Editor = dynamic(
  () => import('react-draft-wysiwyg').then(mod => mod.Editor),
  { ssr: false }
);


export default function OfferConstructor({ws, projectID}: {ws: string, projectID: string}) {
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const closeError = (val: boolean) => setShowError(val);
  const closeSuccess = (val: boolean) => setShowSuccess(val);

  const [editorState, setEditorState] = useState<EditorState>(() => {
    return EditorState.createEmpty();
  });

  let valid = (
      editorState !== undefined && 
      editorState !== undefined 
        ? convertToHTML(editorState.getCurrentContent()).length > 26
        : false
    )

  const getDesc = async () => {
    const res = await project.getProjectDescription(ws, projectID)
    console.log(res)
  }
  
  useEffect(() => {
    getDesc()
  })


  const send = async () => {
    setIsLoading(true)
    const content = convertToHTML(editorState.getCurrentContent());
    const data = JSON.stringify(content)
    const res = await project.setProjectDescription(ws, projectID, data)
    console.log(res)
    res.status == 200 ? (
      setEditorState(undefined as unknown as EditorState), 
      setIsLoading(false),
      setShowSuccess(true)
    ) : (
      setIsLoading(false),
      setShowError(true)
    )
  }

  return (
    <div>
      {showSuccess == true && <Success close={closeSuccess}/>}
      {showError == true && <Error close={closeError}/>}
      <Editor
        editorState={editorState}
        onEditorStateChange={setEditorState}
        wrapperClassName={styles.wrapper}
        editorClassName={styles.editor}
        toolbarClassName={styles.toolbar}
      />
      <div className={styles.confirmButton}>
        {valid == true && <button onClick={() => send()}>Сохранить описание</button>}
      </div>
      {isLoading == true && <LoadingScreen/>}
    </div>
  );
}
