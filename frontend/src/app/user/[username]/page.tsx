'use client'

import React from 'react';
import useSWR from 'swr';
import * as jose from 'jose';
import Link from 'next/link';
import Image from 'next/image';
import LargeHeading from '@/ui/LargeHeading';
import Paragraph from '@/ui/Paragraph';
import { Button, buttonVariants } from '@/ui/Button';
import Icons from '@/components/Icons';

interface PageProps {
  params: {
    username: string
  }
}

const fetcher = async (url: string) => {
  const res = await fetch(url)
  const data = await res.json()
  return data
}

export default function Page ({ params }: PageProps) {
  const { username } = params;
  const userData = useSWR(`/api/${username}`, fetcher);
  const [user, setUser] = React.useState<any>(null);
  const [loggedInUsername, setLoggedInUsername] = React.useState<any>(null);

  let token = null as string | null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('token');
  }

  React.useEffect(() => {
    if (token) {
      const payload = jose.decodeJwt(token);
      if (payload) {
        const user = payload.user as string;
        setLoggedInUsername(user);
      }
    };
  }, [token]);

  React.useEffect(() => {
    if (userData.data) {
      setUser(userData.data);
    }
  }, [userData.data]);

  if (userData.error) return (
    <div className='pt-32'>
      <LargeHeading>
        Error fetching user data
      </LargeHeading>
    </div>
  )

  if (!user) return (
    <div className='pt-32'>
      <LargeHeading>
        Loading...
      </LargeHeading>
    </div>
  )
  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        {
          loggedInUsername === username ? (
            <div className='h-full gap-6 flex flex-col justify-start items-center'>

              <LargeHeading size='lg' className='text-black'>
                My profile
              </LargeHeading>

              <div className='flex flex-col md:flex-col max-w-7xl lg:w-[500px] w-5/12 min-w-[360px] items-center px-8 md:px-0 gap-2 lg:gap-3 pt-6'>
                <div className='flex flex-col justify-start w-full '>
                  <Paragraph size='sm' className='font-medium px-3 w-full text-start'>
                    Profile picture
                  </Paragraph>
                  <Image src={user.profile_picture} alt={user.username} width={100} height={100} className='rounded-full' />
                </div>

                <div className='flex flex-col justify-start w-full '>
                  <Paragraph size='sm' className='font-medium px-3 w-full text-start'>
                    Username
                  </Paragraph>
                  <input
                    type='text'
                    value={user.username}
                    disabled
                    className='bg-gray-200 px-3 w-full py-2 rounded-md opacity-50 cursor-not-allowed' />
                </div>
                <div className='flex flex-col justify-start items-baseline w-full'>
                  <Paragraph size='sm' className='font-medium px-3 w-full text-start'>
                    Email
                  </Paragraph>
                  <input
                    type='email'
                    value={user.email}
                    disabled
                    className='bg-gray-200 px-3 w-full py-2 rounded-md opacity-50 cursor-not-allowed' />
                </div>
                <div className='flex flex-col justify-start items-baseline w-full'>
                  <Paragraph size='sm' className='font-medium px-3 w-full text-start'>
                    Name
                  </Paragraph>
                  <input
                    type='name'
                    value={user.name}
                    disabled
                    className='bg-gray-200 px-3 w-full py-2 rounded-md opacity-50 cursor-not-allowed' />
                </div>
                <div className='flex flex-col md:flex-row max-w-7xl w-full items-center gap-4 md:gap-0 justify-between px-8 md:px-0'>
                  <Link href='/change-password' className={buttonVariants({ variant: 'link' })}>
                    Change password
                  </Link>
                  <Button className='bg-red-600 hover:bg-red-500 ring-red-400 gap-2'>
                    <Icons.Trash /> Delete Account
                  </Button>
                </div>
              </div>
              <div className='flex flex-col items-center w-full gap-4 mt-4' >
                <Link href='/collections' className='flex flex-row items-center text-slate-700 left-0 hover:underline-offset-2 hover:underline sm:text-left'  >
                  View collections <Icons.ChevronRight size={16} />
                </Link>
                <Link href='/recipes' className='flex flex-row items-center text-slate-700 left-0 hover:underline-offset-2 hover:underline sm:text-left'  >
                  View your recipes <Icons.ChevronRight size={16} />
                </Link>
              </div>
            </div>
          ) : (
            <div className='flex flex-col w-full'>
              <div className='w-full gap-6 flex flex-col md:flex-row justify-start md:justify-center items-center'>
                <div className='h-200 w-200'>
                  <Image src={`${user.profile_picture}`} alt={user.name} width={200} height={200} className='rounded-full object-contain' />
                </div>
                <div className='flex flex-col gap-2 items-center'>
                  <LargeHeading size='sm'>
                    {user.name}
                  </LargeHeading>
                  <LargeHeading size='xxs' className='text-slate-700'>
                    {user.username}
                  </LargeHeading>
                  <Paragraph size='sm' className='text-slate-700'>
                    4.6k followers
                  </Paragraph>
                </div>
              </div>
              <div className=''>

              </div>
            </div>
          )
        }
      </div>
    </div>
  );
}
