import project from "@/services/projects";
import { Button, Modal } from "@mantine/core";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function ProjectSettings({
  ws,
  projectID,
}: {
  ws: string;
  projectID: string;
}) {
  
  const router = useRouter()
  const [isModalOpen, setIsModalOpen] = useState(false);

  const deleteProject = async () => {
    await project.deleteProject(ws, projectID).then((res) =>{ 
        setIsModalOpen(!isModalOpen)
        router.push(`/${ws}`)

    })
  }
  return (
    <>
      <Button color="red" variant="outline" onClick={() => setIsModalOpen(!isModalOpen)}>
        Удалить проект
      </Button>

      {isModalOpen === true && (
        <Modal
            opened
            centered
            title={"Удалить проект?"}
            onClose={() => setIsModalOpen(false)}
        >
            <p className="text-sm text-slate-500 mb-4">
                {`Подвердите удаление проекта, нажав кнопку "Удалить"`}
            </p>
            <div className="w-full text-right">
                <Button size="xs" color="red" variant="outline" onClick={() => deleteProject()}>
                    Удалить
                </Button>
            </div>
        </Modal>
      )}

    </>
  );
}
