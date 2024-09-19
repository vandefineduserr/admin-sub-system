import styles from '@/app/[workspace]/[project]/page.module.sass';
import { PickerProps } from '@/interfaces';

export default function LayoutPicker({ cat, catType }: PickerProps) {
  const catArr = [
    { 0: "Оффер" },
    { 1: "Поиск кандидатов" },
    { 2: "Настройки" },
  ];

  return (
    <div className={styles.categoryPicker}>
      {catArr.map((el) => {
        return (
          <div
            className={styles.categoryPickerComponent}
            key={(Object.keys(el)[0])}
          >
            <input
              type="radio"
              name="category-item"
              id={(Object.keys(el)[0])}
              value={(Object.keys(el)[0])}
              onChange={(event) => cat(event.target.value)}
            />
            <label 
              htmlFor={(Object.keys(el)[0])} 
              className={
                catType === Number(Object.keys(el)[0]) ? styles.checked : styles.unChecked
              }
            >
              {Object.values(el)}
            </label>
          </div>
        );
      })}
    </div>
  );
}
