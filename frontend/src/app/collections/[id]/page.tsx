'use client'

import LargeHeading from '@/ui/LargeHeading';
import { useState, useEffect } from 'react';
import useSWR from 'swr';
import { RecipeCard } from '@/components/RecipeCard';
import { Pagination } from '@mui/material';
import Link from 'next/link';

import * as jose from 'jose';

interface PageProps {
  params: { id: string };
}

async function fetcher(url: string) {
  const res = await fetch(url);
  const data = await res.json();
  return data;
}

export default function Page({params}:PageProps) {
  let token = '' as string | null;
  if (typeof(window) !== 'undefined') {
    token = localStorage.getItem('token');
  }
  let user_id = 0;
  let username = '';
  if (token) {
    user_id = jose.decodeJwt(token as string).user_id as number;
    username = jose.decodeJwt(token as string).user as string;
  }

  const { data, error } = useSWR(`/api/${username}/collections/${params.id}`, fetcher);
  const [feedRecipes, setFeedRecipes] = useState<any[]>([]);

  useEffect(() => {

    async function getCollectionRecipes()
    {
      if (feedRecipes != data) {
        setFeedRecipes(data);
      }
    }
    getCollectionRecipes();
  }, [data])

  if (error) return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <LargeHeading>
          Error loading recipes in collection
        </LargeHeading>
      </div>
    </div>
  )
  if (!data) return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <LargeHeading>
          Loading recipes...
        </LargeHeading>
      </div>
    </div>
  )

  if(data != feedRecipes)
  {
    setFeedRecipes(data);
  }
  if(!feedRecipes)
  {
    return (
        <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
          <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
            <LargeHeading>
              Loading...
            </LargeHeading>
          </div>
        </div>
      )
  }

  if(feedRecipes.length == 0)
  {
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
    <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
      <LargeHeading>
        No recipes in this collection
      </LargeHeading>
    </div>
   </div>
  }

  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='h-full gap-8 flex flex-col justify-start items-center'>
          <div className='flex flex-col items-center gap-6 w-full sm:w-4/5 md:w-3/5 lg:2/5'>
            <LargeHeading>
              Browse all Recipes in your Collection
            </LargeHeading>
          </div>
          <div className='h-full flex flex-col justify-start place-items-start px-8 min-w-[360px] w-4/5'>
            {feedRecipes.map((recipe: any) => (
              <Link href={`/recipes/${recipe.recipe_id}`} key={recipe.recipe_id} className='w-full mb-8'>
                <RecipeCard
                  recipeId={recipe.recipe_id}
                  recipeName={recipe.name}
                  recipeImage={recipe.recipe_image}
                  recipeAuthor={recipe.username}
                  recipeDescription={recipe.description}
                  recipeRating={recipe.avgRating}
                  recipeReviewCount={recipe.reviewCount} />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
