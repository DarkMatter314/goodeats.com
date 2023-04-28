'use client'

import React from 'react'
import { useState, useEffect } from 'react';
import Image from 'next/image';
import LargeHeading from '@/ui/LargeHeading';
import NewCollectionDialog from './NewCollectionDialog';
import Paragraph from './myUI/Paragraph';
import { feedCollections, feedRecipes } from '@/public/data';
import useSWR from 'swr';
import * as jose from 'jose';
import { Console } from 'console';
import { FormControlUnstyledContext } from '@mui/base';
import Link from 'next/link';

interface collectionProps {
  secret: string
}

async function fetcher(url: string) {
  const res = await fetch(url);
  const data = await res.json();
  return data;
}




export const UserCollections = ({ secret }: collectionProps) => {
  const [feedCollections, setFeedCollections] = useState<any[]>([]);
  const [username, setUsername] = React.useState('');
  const [user_id, setUserID] = React.useState(0);
  const [session, setSession] = React.useState(false);
  const {data, error } = useSWR(`/api/${username}/collections`, fetcher);

  let token = '' as string | null;
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('token');
  }
  useEffect(() => {
    localStorage.getItem('token') ? setIsAuthenticated(true) : setIsAuthenticated(false);
  }, [token, secret]);

  useEffect(() => {
    const fetchToken = async () => {
      // Check if there's a JWT token in localStorage
      const token = localStorage.getItem('token');
      if (token) {
        const secretKey = new TextEncoder().encode(secret);
        try {
          const { payload, protectedHeader } = await jose.jwtVerify(token, secretKey)
          if (payload) {
            const user = payload.user as string;
            setUsername(user);
            setSession(true);
            setUserID(payload.user_id as number);
          }
        } catch (err) {
          localStorage.removeItem('token');
          setSession(false);
        }
      } else {
        setSession(false);
      }
    }
    fetchToken(); // This is the function that runs every second
    const intervalId = setInterval(fetchToken, 1000);

    if(!username)
    {
      return () => clearInterval(intervalId);
    }
    else
    {
      return () => clearInterval(intervalId);
    }


  }, [secret])



  if (!username || !data) return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <LargeHeading>
          Loading Collections...
        </LargeHeading>
      </div>
    </div>
  )

  if(data != feedCollections)
  {
    setFeedCollections(data);
  }
  //else we set the collection
  if (token === '') return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden pb-32'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='flex flex-col items-center'>
          <LargeHeading>
            Loading...
          </LargeHeading>
        </div>
      </div>
    </div>
  )

  if (!isAuthenticated) return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden pb-32'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='flex flex-col items-center'>
          <LargeHeading>
            You must be logged in to view this page
          </LargeHeading>
        </div>
      </div>
    </div>
  )

  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden pb-32'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='h-full gap-8 flex flex-col justify-start items-center'>
          <div className='flex flex-row items-center gap-6'>
            <LargeHeading>
              My Collections
            </LargeHeading>
            <NewCollectionDialog username={username} user_id={user_id} />
          </div>
          <div className='h-full flex flex-col justify-start items-center w-full px-8'>
            {
              feedCollections.length == 0 ? (
                <div className='flex flex-col items-center'>
                  <LargeHeading size='xs'>
                    You have no collections
                  </LargeHeading>
                  <Paragraph>
                    Create a new collection to get started
                  </Paragraph>
                </div>
              ) : feedCollections.map((collection) => (

                // <Link href={`/collections/${collection.collectionId}`} key={collection.collectionId}>
                <Link href={`/collections/${(collection.collection_id).toString()}`} key={collection.collection_id} className='flex flex-col items-center md:items-start md:flex-row gap-4 md:w-[720px] lg:w-[900px] max-w-7xl pb-6'>
                  <div className=''>
                    <LargeHeading size='xs' > {collection.cn} </LargeHeading>
                    <Image
                      src={collection.collection_image}
                      height={250}
                      width={300}
                      alt='thumbnail'
                      className='rounded-xl'
                    />
                  </div>
                  <div className='flex flex-col gap-1 w-[250px] md:w-full'>
                    <LargeHeading className='text-start' size='xs'>
                      {collection.collection_name}
                    </LargeHeading>
                    <Paragraph size='sm' className='text-start'>
                      {collection.description}
                    </Paragraph>
                  </div>
                </Link>

              )


              )
            }
          </div>
        </div>
      </div>
    </div>
  )
}
