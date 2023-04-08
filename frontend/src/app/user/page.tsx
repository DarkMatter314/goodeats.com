import LargeHeading from '@/components/ui/LargeHeading';
import React from 'react';
import { Metadata } from 'next'
import Paragraph from '@/components/ui/Paragraph';
import { Button, buttonVariants } from '@/components/ui/Button';
import Link from 'next/link';
import Icons from '@/components/Icons';

export const metadata: Metadata = {
  title: 'Goodeats | My profile',
}

const page: React.FC = () => {
  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='h-full gap-6 flex flex-col justify-start items-center'>

          <LargeHeading size='lg' className='text-black'>
            My profile
          </LargeHeading>

          <div className='flex flex-col md:flex-col max-w-7xl lg:w-[500px] w-5/12 items-center px-8 md:px-0 gap-2 lg:gap-3 pt-6'>
            <div className='flex flex-col justify-start w-full '>
              <Paragraph size='sm' className='font-medium px-3 w-full text-start'>
                Username
              </Paragraph>
              <input
              type='text'
              value='username'
              disabled
              className='bg-gray-200 px-3 w-full py-2 rounded-md opacity-50 cursor-not-allowed' />
            </div>
            <div className='flex flex-col justify-start w-full'>
              <Paragraph size='sm' className='font-medium px-3 w-full text-start'>
                Email
              </Paragraph>
              <input
              type='email'
              value='email'
              disabled
              className='bg-gray-200 px-3 w-full py-2 rounded-md opacity-50 cursor-not-allowed' />
            </div>
            <div className='flex flex-col justify-start w-full'>
              <Paragraph size='sm' className='font-medium px-3 w-full text-start'>
                Name
              </Paragraph>
              <input
              type='name'
              value='name'
              disabled
              className='bg-gray-200 px-3 w-full py-2 rounded-md opacity-50 cursor-not-allowed' />
            </div>
            <div className='flex flex-col md:flex-row max-w-7xl w-full items-center gap-4 md:gap-0 justify-between px-8 md:px-0'>
            <Link href='/change-password' className={buttonVariants({ variant: 'link' })}>
              Change password
            </Link>
            <Button className='flex flex-row items-center gap-2 bg-orange-300 hover:bg-orange-200 text-black'>
              <Icons.Trash /> Delete Account
            </Button>
          </div>
          <div className='h-5 md:h-7 lg:h-9'></div>
          <div className='justify-start left-1 w-full gap-4' ></div>
          <Link href='/collections' className='flex flex-row items-center text-slate-700 left-0 hover:underline-offset-2 hover:underline sm:text-left'  >
               View collections <Icons.ChevronRight size={16} />
          </Link>
          <Link href='/recipes' className='flex flex-row items-center text-slate-700 left-0 hover:underline-offset-2 hover:underline sm:text-left'  >
               View your recipes <Icons.ChevronRight size={16} />
          </Link>

          </div>



        </div>
      </div>
    </div>
  );
}

export default page
