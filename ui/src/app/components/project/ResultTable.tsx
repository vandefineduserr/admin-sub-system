//system
import React, { useLayoutEffect, useState } from "react";

//services
import { EditButton } from "@/app/components/buttons/buttons";

//styles
import styles from "@/app/[workspace]/[project]/page.module.sass";
import ai from "@/services/ai";

function TableHeader() {
  return (
    <tr key={"header"}>
      <th>#</th>
      <th>Имя</th>
      <th>Возраст</th>
      <th>Пол</th>
      <th>Профессия</th>
      <th>Регион</th>
      <th>Стаж</th>
      <th>Зарплата</th>
      <th>Актуальность</th>
      <th></th>
    </tr>
  );
}

function TableButtons({ data }: any) {
  const [openFullResume, setIsOpen] = useState(false);
  const isEditOpen = (val: boolean) => setIsOpen(val);

  return (
    <div className={styles.tableButtons}>
      <button onClick={() => setIsOpen(true)}>
        <EditButton />
      </button>
      {openFullResume === true && (
        <SingleCV element={data} isOpen={isEditOpen} />
      )}
    </div>
  );
}

function SingleCV(element: any) {
  const [cv, setCv] = useState<any>(element.element);
  const [x, setX] = useState<number>(0);

  const findX = async () => {
    console.log('x')
    await ai
      .rateCandidate(cv)
      .then(({ data }: any) => setX(data))
      .catch((e) => console.log(e));
  };

  useLayoutEffect(() => {
    setCv(element.element);
  });

  return (
    <div className="cv-container">
      <div className="cv-page">
        <div className="cv-header">
          {/* onClick={() => isOpen(false)} */}
          <button className={styles.closeBtn}>Закрыть</button>
          <h3>{cv.name}</h3>
          <h4>{cv.profession}</h4>
          <h4>{cv.salary}</h4>
        </div>
        <div className="cv-block">
          <span>Информация о кандидате</span>
          <hr />
          <p>Пол: {cv.gender}</p>
          <p>Возраст: {cv.age}</p>
          <p>Проживает: {cv.area}</p>
          <p>Гражданство: {cv.citizenship}</p>
          <p>Персональные данные: {cv.schedule}</p>
        </div>
        <div className="cv-block">
          <span>Ключевые навыки</span>
          <hr />
          <p>Навыки: {cv.skills}</p>
          <p>Языки: {cv.languages}</p>
          <p>Права: {cv.car}</p>
        </div>
        <div className="cv-block">
          <span>Опыт работы - {cv.in_service}</span>
          <hr />
          {cv.work_experience ? (
            cv.work_experience.map((el: any, index: number) => {
              return (
                <div className="exp-block" key={index}>
                  <p>Позиция: {el.position}</p>
                  <p>Название компании: {el.company}</p>
                  <p>Срок: {el.job_period}</p>
                  {/* <p>
                    Обязанности: {el.duties.toString()}
                  </p> */}
                </div>
              );
            })
          ) : (
            <></>
          )}
        </div>
        <div className="cv-block">
          <a href={cv.cv_link}>{cv.cv_link}</a>
          <br />
          {x ? (
            <p>Кандидат подходит на {x}% </p>
          ) : (
            <button onClick={() => findX()}>Оценить резюме</button>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ResultTable({ forms }: any) {
  const render = () => {
    return forms.map((el: any, index: number) => {
      return (
        <tr key={index}>
          <td>{index + 1}</td>
          <td>{el.name}</td>
          <td>{el.age}</td>
          <td>{el.gender}</td>
          <td className={styles.abbriviatedText}>{el.profession}</td>
          <td>{el.area}</td>
          <td>{el.in_service}</td>
          <td>{el.salary}</td>
          <td>{el.actuality}</td>

          <td>
            <TableButtons data={el} />
          </td>
        </tr>
      );
    });
  };

  return (
    <table className={styles.resTable}>
      <tbody>
        <TableHeader />
        {render()}
      </tbody>
    </table>
  );
}
