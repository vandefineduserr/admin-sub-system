//system
import { useState } from "react";
import { useForm } from "react-hook-form";

// components
import Success from "../notfications/success";
import Error from "../notfications/error";

//services
import {
  cities,
  employmentTypes,
  educationTypes,
  carCategory,
  workSchedule,
} from "@/services/constants";

//styles
import styles from "@/app/[workspace]/[project]/page.module.sass";
import parsing from "@/services/parsing";


export default function RequestForm({ ws_name, project }: any) {
  const { register, handleSubmit } = useForm();

  // notification
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const closeError = (val: boolean) => setShowError(val);
  const closeSuccess = (val: boolean) => setShowSuccess(val);

  const onSubmit = async (data: any) => {
    const res = await parsing.findCandidates(data, ws_name, project);
    res.status === 200 ? setShowSuccess(true) : setShowError(true);
  };

  return (
    <>
      {showSuccess == true && <Success close={closeSuccess} />}
      {showError == true && <Error close={closeError} />}
      <div className={styles.requestForm}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className={styles.row}>
            <input
              id={styles.formTitle}
              {...register("keywords")}
              placeholder="Кого необходимо найти?"
              type="text"
              required
            />
            <button className={styles.resumeButton}>Найти</button>
          </div>

          <select
            id={styles.formRegionSelector}
            {...register("region")}
            defaultValue={"Везде"}
            required
          >
            {cities.map((el) => {
              return (
                <option key={el} value={el}>
                  {el}
                </option>
              );
            })}
          </select>

          <details>
            <summary>Расширенный поиск</summary>

            {/* salary */}
            <div className={styles.formBlock}>
              <h4>Зарплата</h4>
              <div className={styles.row}>
                <span>от</span>
                <input
                  {...register("min_salary")}
                  placeholder="Мин. зарплата"
                  type="text"
                />
                <span>до</span>
                <input
                  {...register("max_salary")}
                  placeholder="Макс. зарплата"
                  type="text"
                />
              </div>
            </div>

            {/* age */}
            <div className={styles.formBlock}>
              <h4>Возраст</h4>
              <div className={styles.row}>
                <span>от</span>
                <input
                  type="text"
                  {...register("age_min")}
                  placeholder="Мин. возраст"
                />
                <span>до</span>
                <input
                  type="text"
                  {...register("age_max")}
                  placeholder="Макс. возраст"
                />
              </div>
            </div>

            {/* gender */}
            <div className={styles.formBlock}>
              <h4>Пол</h4>
              <select {...register("sex")} defaultValue={"Любой"}>
                <option key={"Любой"} value="Любой">
                  Любой
                </option>
                <option key={"Мужской"} value="Мужской">
                  Мужской
                </option>
                <option key={"Женский"} value="Женский">
                  Женский
                </option>
              </select>
            </div>

            {/* employment */}
            <div className={styles.formBlock}>
              <h4>Занятость</h4>
              <select
                {...register("employment")}
                defaultValue={employmentTypes[0]}
              >
                {employmentTypes.map((el) => {
                  return (
                    <option key={el} value={el}>
                      {el}
                    </option>
                  );
                })}
              </select>
            </div>

            {/* work schedule */}
            <div className={styles.formBlock}>
              <h4>График работы</h4>
              <select
                {...register("work_schedule")}
                defaultValue={workSchedule[0]}
              >
                {workSchedule.map((el) => {
                  return (
                    <option key={el} value={el}>
                      {el}
                    </option>
                  );
                })}
              </select>
            </div>

            {/* in service */}
            <div className={styles.formBlock}>
              <h4>Стаж</h4>
              <div className={styles.row}>
                <span>от</span>
                <input
                  {...register("in_service_min")}
                  type="text"
                  placeholder="Стаж (мин.)"
                />
                <span>до</span>
                <input
                  {...register("in_service_max")}
                  type="text"
                  placeholder="Стаж (макс.)"
                />
              </div>
            </div>

            {/* education */}
            <div className={styles.formBlock}>
              <h4>Образование</h4>
              <select
                {...register("education")}
                defaultValue={educationTypes[0]}
              >
                {educationTypes.map((el) => {
                  return (
                    <option key={el} value={el}>
                      {el}
                    </option>
                  );
                })}
              </select>
            </div>

            {/* state */}
            <div className={styles.formBlock}>
              <h4>Гражданство</h4>
              <input
                {...register("citizenship")}
                type="text"
                placeholder="Гражданство"
              />
              <br />
              <h4>Разрешение на работу</h4>
              <input
                {...register("work_permit")}
                type="text"
                placeholder="Разрешение на работу"
              />
            </div>

            <div className={styles.formBlock}>
              <h4>Категория прав</h4>
              <select
                {...register("car_category")}
                defaultValue={carCategory[0]}
                required
              >
                {carCategory.map((el) => {
                  return (
                    <option key={el} value={el}>
                      {el}
                    </option>
                  );
                })}
              </select>
              <label>
                <input
                  {...register("car")}
                  name="car"
                  id="car"
                  type="checkbox"
                />
                <span>Личный автомобиль</span>
              </label>
            </div>

            <div className={styles.formBlock}></div>
          </details>

          {/* <div className={styles.row}>
          <input
            {...register("languages")}
            type="text"
            placeholder="Языки"
            required
          />
          <br />
          <input
            {...register("skills")}
            type="text"
            placeholder="Навыки"
            required
          />
        </div> */}
        </form>
      </div>
    </>
  );
}
