'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import useSWR from 'swr'
import * as jose from 'jose'
import LargeHeading from '@/ui/LargeHeading'
import { ScrollArea } from '@/components/RecipeSlide'
import { feedRecipes } from '@/public/data'

async function fetcher(url: string) {
  const res = await fetch(url);
  const data = await res.json();
  return data;
}

async function recommendFetcher(url: string) {
  let token = null as string | null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('token');
  }
  let user_id = -1;
  if (token) {
    const payload = jose.decodeJwt(token);
    if (payload) {
      user_id = payload.user_id as number;
    }
  };
  if (user_id === -1) {
    return { recipe_data: [] };
  }
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({user_id}),
  });
  const data = await res.json();
  return data;
}

export default function Home() {
  const topRecipesData = useSWR('/api/top_rated', fetcher);
  const recommendedRecipesData = useSWR('/api/recommend_recipes', recommendFetcher);
  const [topRecipes, setTopRecipes] = useState<any[]>(topRecipesData.data || []);
  const [recommendedRecipes, setRecommendedRecipes] = useState<any[]>(recommendedRecipesData.data || []);

  useEffect(() => {
    if (topRecipesData.data) {
      setTopRecipes(topRecipesData.data.recipe_data);
    }
  }, [topRecipesData.data])

  useEffect(() => {
    if (recommendedRecipesData.data?.recipe_data) {
      if (recommendedRecipesData.data.recipe_data.length > 10) {
        setRecommendedRecipes(recommendedRecipesData.data.recipe_data.slice(0, 10));
      } else {
        setRecommendedRecipes(recommendedRecipesData.data.recipe_data);
      }
    }
  }, [recommendedRecipesData.data])

  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden bg-slate-200 overflow-y-auto'>
      <div className='container pt-32 max-w-full w-full h-full'>
        <div className='h-full w-full gap-6  flex md:flex-row flex-col justify-start lg:justify-center items-center lg:items-start rounded-md'>

          <div className='relative md:w-1/2 sm:w-full gap-10 flex flex-col h-[530px] items-center justify-center '>
            <LargeHeading className='font-semibold '>
              Looking for a snack?
            </LargeHeading>
            <LargeHeading className='text-wrap font-semibold' size='sm'>
              Whether you want easy to make homemade food or exquisite dishes and delicacies, We&apos;ve got you covered.
            </LargeHeading>
            <LargeHeading className='font-semibold'>
              Welcome to GoodEats!
            </LargeHeading>
          </div>

          <div className='md:w-1/2 align-middle justify-center w-3/4  h-[600px]'>
            <Image className='align-middle w-full h-600 object-cover' src='/fryingpantop.jpg' alt='frying pan' width={1000} height={1000} />
          </div>
        </div>

        {
          !topRecipesData.error && topRecipes && topRecipes.length > 0 && (
            <ScrollArea key={1} feedRecipes={topRecipes} header='Top Rated' />
          )
        }

        {
          !recommendedRecipesData.error && recommendedRecipes && recommendedRecipes.length > 0 && (
            <ScrollArea key={2} feedRecipes={recommendedRecipes} header='Recommended for you' />
          )
        }

        <div className='flex flex-row justify-center md:h-[500px] sm:h-[300px] h-[200px] items-center gap-6 bg-slate-300'>
          <Link href='/recipes' className='flex flex-col justify-center h-2/3 lg:w-1/4 md:w-1/3 w-3/6 items-center hover:scale-102 hover:shadow-2xl hover:bg-gray-700  bg-blackA11 rounded-3xl align-middle'>
            <LargeHeading size={'bottom'} className='font-light w-4/5 align-middle text-[#FFDCDC]'>
              Want something more appetising? <br />
              View all recipes
            </LargeHeading>
          </Link>

          <Link href='/post-recipe' className='flex flex-col justify-center h-2/3 lg:w-1/4 md:w-1/3 w-3/6 items-center hover:scale-102 hover:shadow-2xl hover:bg-gray-700 bg-blackA11 rounded-3xl align-middle'>
            <LargeHeading size={'bottom'} className='font-light w-4/5 align-middle text-[#FFDCDC]'>
              Got a new creation? <br />
              Post it here!
            </LargeHeading>
          </Link>

        </div>
      </div>
    </div>
  )

}
