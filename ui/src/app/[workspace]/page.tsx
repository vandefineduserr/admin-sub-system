//system
"use client";
import { useEffect, useState } from "react";
import {
  createStyles,
  Card,
  Image,
  Text,
  Group,
  RingProgress,
  rem,
  Header,
  Code,
  Button,
  Container,
  Modal,
  TextInput,
  Textarea,
} from "@mantine/core";
import workspace from "@/services/workspace";
import { Project, Workspace } from "@/interfaces";
import { useForm } from "@mantine/form";
import project from "@/services/projects";
import Link from "next/link";
import parsing from "@/services/parsing";
import { WorkspaceContext } from "@/contexts";



const HEADER_HEIGHT = rem(40);
const DEFAULT = "https://images.unsplash.com/photo-1596434220574-9af8bf9a0891?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2928&q=808";
const useStyles = createStyles((theme) => ({
  inner: {
    height: HEADER_HEIGHT,
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  card: {
    backgroundColor:
      theme.colorScheme === "dark" ? theme.colors.dark[7] : theme.white,
  },

  footer: {
    display: "flex",
    justifyContent: "space-between",
    padding: `${theme.spacing.sm} ${theme.spacing.lg}`,
    borderTop: `${rem(1)} solid ${
      theme.colorScheme === "dark" ? theme.colors.dark[5] : theme.colors.gray[2]
    }`,
  },

  title: {
    fontFamily: `Greycliff CF, ${theme.fontFamily}`,
    lineHeight: 1,
  },
}));

function CardWithStats({project}: {project: Project}) {
  const { classes } = useStyles();
  const stats = [project.creationDate]
  const items = stats.map((stat) => (
    <div key={stat}>
      <Text size="xs" color="dimmed">
        Дата
      </Text>
      <Text weight={500} size="sm">
        {stat}
      </Text>
    </div>
  ));

  return (
    <Card withBorder padding="lg" className={classes.card} radius="md">
      <Card.Section>
        <Image src={project.layout == "" ? DEFAULT: project.layout} alt={"project_hero"} height={150} />
      </Card.Section>

      <Group position="apart" mt="xl">
        <Text fz="sm" fw={700} className={classes.title}>
          {project.name}
        </Text>
      </Group>
      <Text mt="sm" mb="md" c="dimmed" fz="xs">
        {project.description}
      </Text>
      <Card.Section className={classes.footer}>{items}</Card.Section>
    </Card>
  );
}

export default function WorkspaceComponent({
  params,
}: {
  params: { workspace: string };
}) {
  const { classes } = useStyles();
  const [ws, setWorkspace] = useState<Workspace>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newProjectModal, setNewProjectModal] = useState(false);
  const [parsersAvailability , setParsersAvailability] = useState<string | undefined>()

  const form = useForm({
    initialValues: {
      name: "",
      description: "",
      layout: "",
    },

    validate: {
      name: (val) =>
        val.length <= 6 && val.length >= 50
          ? "Имя проекта должно быть не менее 6 и не более 50 символов"
          : null,
    },
  });

  useEffect(() => {
    const parse = async () => {
      parsing.checkParsersAvailability()
        .then((res) => setParsersAvailability(res.data.echo))
    };

    const getWorkspaceInfo = async () => {
      setWorkspace((await workspace.getWorkspaceInfo(params.workspace))?.data);
    };

    getWorkspaceInfo();
    parse();

  }, [params.workspace]);

  const createNewProject = async (form: any) => {
    setIsSubmitting(true)
    const res = await project.createProject(params.workspace, form)
    setWorkspace((await workspace.getWorkspaceInfo(params.workspace))?.data);
    setNewProjectModal(false);
  };

  console.log(params.workspace)

  return (
    <WorkspaceContext.Provider value={params.workspace}>
      <Header height={HEADER_HEIGHT} mt={8}>
        <Container className={classes.inner} fluid>
          <Code p={4} sx={{ fontWeight: 700 }}>
            {ws?.name}
          </Code>
          <Code p={4} sx={{ fontWeight: 700 }}>
            {parsersAvailability}
          </Code>
          <Button
            variant="outline"
            radius="xl" 
            h={25} 
            onClick={() => setNewProjectModal(true)}
          >
            Новый проект
          </Button>
        </Container>
      </Header>
      <div className="p-4 grid grid-cols-3 gap-4">
        {ws?.projectsDetails && ws?.projectsDetails?.length > 0
          ? ws?.projectsDetails.map((el: any) => {
              return (
                <Link href={`/${params.workspace}/${el.uid}`} key={el.uid}>
                  <CardWithStats
                    project={el as Project}
                    key={el.uid}
                  />
                </Link>
              );
            })
          : "Нет ни одного проекта"}
      </div>

      {newProjectModal == true && (
        <Modal
          title={"Новый проект"}
          opened
          centered
          onClose={() => setNewProjectModal(false)}
        >
          <form onSubmit={form.onSubmit(() => {})}>
            <TextInput
              required
              label="Имя"
              placeholder="Имя проекта"
              value={form.values.name}
              onChange={(event) =>
                form.setFieldValue("name", event.currentTarget.value)
              }
              error={form.errors.email && "Неверный email"}
              radius="md"
              mb={16}
            />
            <TextInput
              label="Обложка"
              placeholder="Ссылка на изображение"
              value={form.values.layout}
              onChange={(event) =>
                form.setFieldValue("layout", event.currentTarget.value)
              }
              radius="md"
              mb={16}
            />
            <Textarea
              label="Описание"
              placeholder="Описание проекта"
              rows={5}
              value={form.values.description}
              onChange={(event) =>
                form.setFieldValue("description", event.currentTarget.value)
              }
              radius="md"
              mb={16}
            />

            <Button
              fullWidth
              mt="md"
              radius="md"
              type="submit"
              variant="outline"
              onClick={() => createNewProject(form.values)}
              disabled={form.isValid() == false}
            >
              {isSubmitting == true ? 'Создание...' : 'Создать'}
            </Button>
          </form>
        </Modal>
      )}
    </WorkspaceContext.Provider>
  );
}
