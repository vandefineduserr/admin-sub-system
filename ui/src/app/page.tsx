"use client";
import CryptoJS from "crypto-js";
import styles from "./page.module.sass";
import Image from "next/image";
import axios from "axios";
import { useRouter } from "next/navigation";
import Authorization from "@/services/authorisation";
import { useToggle, upperFirst } from "@mantine/hooks";
import { useForm } from "@mantine/form";
import {
  TextInput,
  PasswordInput,
  Group,
  Button,
  Checkbox,
  Anchor,
  Stack,
} from "@mantine/core";
import myProfile from "@/services/me";

function Login() {
  const router = useRouter();

  const [type, toggle] = useToggle(["login", "register"]);
  const form = useForm({
    initialValues: {
      firstname: "",
      lastname: "",
      email: "",
      password: "",
      terms: true,
    },

    validate: {
      email: (val) => (/^\S+@\S+$/.test(val) ? null : "Неверный email"),
      password: (val) =>
        val.length <= 6
          ? "Пароль должен быть не менее 6 символов"
          : null,
    },
  });


  const login = (form: any) => {
    axios
      .post("/api/login", {
        email: form.values.email,
        password: CryptoJS.SHA256(form.values.password).toString(CryptoJS.enc.Hex),
      })
      .then(async (res) => { 
        if (!res.data.token) return;

        Authorization.setAccessToken(res.data.token);

        const me = await myProfile.getMyInfo()
        router.push(`${me.data.workspaces[0] === undefined 
          ? "/boarding" : me.data.workspaces[0] }`)

      });
  }

  const register = (form: any) => {
    axios
      .post("/api/register", {
        email: form.values.email,
        password: CryptoJS.SHA256(form.values.password).toString(CryptoJS.enc.Hex),
        firstname: form.values.firstname,
        lastname: form.values.lastname,
      })
      .then(async (res) => { 
        if (!res.data.token) return;

        Authorization.setAccessToken(res.data.token);

        const me = await myProfile.getMyInfo()
        router.push(`${me.data.workspaces[0] === undefined ? "/boarding" : me.data.workspaces[0] }`)

      });
  }


  return (
    <div className={styles.loginForm}>

      <h2>Добро пожаловать!</h2>
      <p>Введите логин и пароль, чтобы войти</p>
      <form onSubmit={form.onSubmit(() => {})}>
        <Stack>
          {type === "register" && (
            <>
              <TextInput
                label="Имя"
                placeholder="Ваше имя"
                value={form.values.firstname}
                onChange={(event) =>
                  form.setFieldValue("firstname", event.currentTarget.value)
                }
                radius="md"
              />

              <TextInput
                label="Фамилия"
                placeholder="Ваша фамилия"
                value={form.values.lastname}
                onChange={(event) =>
                  form.setFieldValue("lastname", event.currentTarget.value)
                }
                radius="md"
              />
            </>
          )}

          <TextInput
            required
            label="Email"
            placeholder="hello@example.dev"
            value={form.values.email}
            onChange={(event) =>
              form.setFieldValue("email", event.currentTarget.value)
            }
            error={form.errors.email && "Неверный email"}
            radius="md"
          />

          <PasswordInput
            required
            label="Пароль"
            placeholder="Ваш пароль"
            value={form.values.password}
            onChange={(event) =>
              form.setFieldValue("password", event.currentTarget.value)
            }
            error={
              form.errors.password &&
              "Пароль должен быть не менее 6 символов"
            }
            radius="md"
          />

          {type === "register" && (
            <Checkbox
              label="Я принимаю условия использования"
              checked={form.values.terms}
              onChange={(event) =>
                form.setFieldValue("terms", event.currentTarget.checked)
              }
            />
          )}
        </Stack>

        <Group position="apart" mt="xl">
          <Anchor
            component="button"
            type="button"
            color="dimmed"
            onClick={() => toggle()}
            size="xs"
          >
            {type === "register"
              ? "Есть аккаунт? Войти"
              : "Нет аккаунта? Регистрация"}
          </Anchor>
          <Button 
            type="submit" 
            variant="outline" 
            radius="xl" 
            onClick={() => {type === "register" ? register(form) : login(form)}}
          >
            {upperFirst(type)}
          </Button>
        </Group>
      </form>
    </div>
  );
}

export default function AdminLoginPage() {
  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <div className={styles.row}>
          <div className={styles.column}>
            <div className={styles.loginLayout}>
              <Login />
            </div>
          </div>
          <div className={styles.column}>
            <Image
              className={styles.loginImg}
              src="/login-hero.jpg"
              alt="admin-hero"
              height={1000}
              width={1000}
            />
          </div>
        </div>
      </div>
    </main>
  );
}