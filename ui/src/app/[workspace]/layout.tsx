"use client"
import '../globals.css'
import { Inter } from 'next/font/google'
import NavbarNext from '../components/navbar/navbar'
import React from 'react'

const inter = Inter({ subsets: ['latin'] })


export default function RootLayout({children, params}: {
  children: React.ReactNode,
  params: { workspace: string };
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className='fixed top-0 left-0 w-[300px] h-screen'>
          <NavbarNext ws={params.workspace}/>
        </div>
        <div className='absolute top-0 left-[300px] w-[calc(100vw-300px)]'>
          { children }
        </div>      
      </body>
    </html>
  )
}
