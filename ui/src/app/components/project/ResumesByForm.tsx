//components
import { Button } from "@mantine/core";
import RequestForm from "./RequestForm";
import ResultTable from "./ResultTable";

//styles
import styles from "@/app/[workspace]/[project]/page.module.sass";

export default function ResumesByForm({
  forms,
  workspaceName,
  projectName,
}: any) {
  function downloadURI() {
    const link = document.createElement('a');
    link.href = `/api/project/${workspaceName}/${projectName}/download/table`;
    link.setAttribute('download', `sample.csv`);
    document.body.appendChild(link);
    link.click();
  }

  return (
    <div>
      <div className={styles.row}>
        <RequestForm ws_name={workspaceName} project={projectName} />
      </div>

      <br />

      {forms.length > 0 ? (
        <>
          <Button
            mt="md"
            radius="md"
            variant="outline"
            onClick={() => downloadURI()}
          >
            Скачать таблицу
          </Button>
          <ResultTable forms={forms} />
        </>
      ) : (
        <p>Загрузка данных</p>
      )}
    </div>
  );
}
