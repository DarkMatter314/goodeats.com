import * as React from 'react'
import LargeHeading from '@/ui/LargeHeading'
import Image from 'next/image'
import About from '@/components/About'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Goodeats | About Us',
}

const imageSize = 400;
const page: React.FC = () => {
  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='h-full gap-6 flex flex-col justify-start items-center'>
          <LargeHeading size='lg'>
            About Us
          </LargeHeading>

          <div className='flex flex-col lg:flex-row justify-center gap-4 md:gap-20 items-start'>

            <div className='flex flex-row md:flex-row justify-center items-start gap-4 md:gap-20'>

              <About Name='Dhruv Ahlawat' Role='Full Stack Developer'
                ImagePath='/MyPhoto.jpeg' imageSize={imageSize} Description='the Brains behind the project'
                GithubIds='DhruvAhlawat' />

              <About Name='Rishabh Verma' Role='Frontend Master'
                ImagePath='/Rishabh.png' imageSize={imageSize} Description='The reason why we banged our heads over learning Tailwind and Typescript and Nextjs'
                GithubIds='rish106' />

            </div>

            <div className='flex flex-row md:flex-row justify-center items-start gap-4 md:gap-20 pb-8'>

              <About Name='Garv Nagori' Role='Flask video watcher'
                ImagePath='/Rishabh.png' imageSize={imageSize} Description='Learnt Flask from youtube'
                GithubIds='DarkMatter314' />

              <About Name='Naman Agarwal' Role='ER diagram expert'
                ImagePath='/Rishabh.png' imageSize={imageSize} Description='made ER diagrams and (possibly?) did MySQL'
                GithubIds='Naman0411' />

            </div>

          </div>
        </div>
      </div>
    </div>
  )
}

export default page
