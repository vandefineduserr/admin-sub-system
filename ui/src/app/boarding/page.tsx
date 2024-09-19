"use client";

import { Button, Modal, Select, TextInput, Textarea } from "@mantine/core";
import styles from "./page.module.sass";
import Image from "next/image";
import { useState } from "react";
import { useForm } from "@mantine/form";
import workspace from "@/services/workspace";
import { useRouter } from "next/navigation";

export default function Boarding() {
  const router = useRouter()
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newProjectModal, setNewProjectModal] = useState(false);

  const form = useForm({
    initialValues: {
      name: "",
      type: 1,
      members: [],
      invitations: [],
      projects: [],
      projectsDetails: [],
      tasks: []
    },

    validate: {
      name: (val) =>
        val.length <= 6 && val.length >= 50
          ? "Имя пространства должно быть не менее 6 и не более 50 символов"
          : null,
    },
  });

  const createNewWS = (data: any) => {
    workspace.createWorkspace(data).then((res: any) => {
      res.status === 200 ? router.push(`/${res.data.ws_name}`) : null
    })
  }

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <Button variant="outline" onClick={() => setNewProjectModal(true)}>Создать пространство</Button>
        {newProjectModal == true && (
          <Modal
            title={"Новое пространство"}
            opened
            centered
            onClose={() => setNewProjectModal(false)}
          >
            <form onSubmit={form.onSubmit(() => {})}>
              <TextInput
                required
                label="Имя"
                placeholder="Имя пространства"
                value={form.values.name}
                onChange={(event) =>
                  form.setFieldValue("name", event.currentTarget.value)
                }
                error={form.errors.email && "Неверный email"}
                radius="md"
                mb={16}
              />

              <Select
                label="Выберите тип пространства"
                placeholder="Выберите"
                data={[
                  { value: "1", label: 'Персональное' },
                  // { value: "2", label: 'Персональное +' },
                  { value: "3", label: 'Бизнес' },
                  // { value: "4", label: 'Бизнес +' },
                ]}
                maxDropdownHeight={200}
                onChange={(event) =>
                  form.setFieldValue("type", 3)
                }
              />

              <Button
                fullWidth
                mt="md"
                radius="md"
                type="submit"
                variant="outline"
                onClick={() => createNewWS(form.values)}
                disabled={form.isValid() == false}
              >
                {isSubmitting == true ? "Создание..." : "Создать"}
              </Button>
            </form>
          </Modal>
        )}
      </div>
    </main>
  );
}
