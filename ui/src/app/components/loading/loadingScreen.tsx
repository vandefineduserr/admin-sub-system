import styles from './loading.module.sass'
import Image from 'next/image'

export default function LoadingScreen(){
    return (
        <div className={styles.underlay}>
            <div className={styles.overlay}>
                <Image
                    src="/images/loading.gif"
                    alt="nav"
                    height={150}
                    width={150}
                />
            </div>
        </div>
    )
}