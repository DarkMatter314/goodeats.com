'use client'

import Image from 'next/image';
import useSWR from 'swr';
import React from 'react';
import * as jose from 'jose';
import LargeHeading from '@/ui/LargeHeading';
import Paragraph from '@/ui/Paragraph';
import Icons from '@/components/Icons';
import CommentForm from '@/components/CommentForm';
import { RecipeActions } from '@/components/RecipeActions';
import { CommentCard } from '@/components/CommentCard';
import Link from 'next/link';

interface ingredient {
  amount: string;
  name: string;
}

interface PageProps {
  params: { id: string };
}

const fetcher = async (url: string) => {
  const res = await fetch(url)
  const data = await res.json()
  return data
}

const commentFetcher = async (url: string) => {
  const token = localStorage.getItem('token');
  let user_id = 0;
  if (token) {
    user_id = jose.decodeJwt(token as string).user_id as number;
  }
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(user_id ? { user_id } : {}),
  })
  const data = await res.json();
  if (data.error) {
    return {user_reviews: [], other_reviews: []};
  } else {
    return data;
  }
}

const Page = ({ params }: PageProps) => {

  const recipeData = useSWR(`/api/recipe/${params.id}`, fetcher)
  const commentData = useSWR(`/api/recipe/${params.id}/reviews`, commentFetcher)
  const [comments, setComments] = React.useState<any>([]);
  const [post, setPost] = React.useState<any>(null);

  React.useEffect(() => {
    if (recipeData.data && commentData.data) {
      setPost(recipeData.data);
      setComments([...commentData.data.user_reviews, ...commentData.data.other_reviews]);
    }
  }, [recipeData.data, commentData.data])

  if (recipeData.error || commentData.error || recipeData.data?.error) return (
    <div className='pt-32'>
      <LargeHeading>
        Error fetching recipe data
      </LargeHeading>
    </div>
  )

  if (!post || !comments) return (
    <div className='pt-32'>
      <LargeHeading>
        Loading...
      </LargeHeading>
    </div>
  )

  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container max-w-full mx-auto w-full h-full'>
        <div className='h-full gap-0 flex flex-col justify-start items-center'>
          <div className='flex pt-32 flex-col-reverse justify-between items-center gap-8 md:flex-row md:px-10 bg-slate-800 min-h-screen w-full px-8 pb-8'>
            <div className='flex flex-col md:w-1/2 justify-center gap-3 items-center'>
              <LargeHeading className='text-white text-center w-full'>
                {post.recipe_data.name}
              </LargeHeading>
              <Link href={`/user/${post.user_data.username}`} className='text-xl md:text-2xl lg:text-3xl text-white font-bold'>
                {post.user_data.username}
              </Link>
              <div className='flex flex-row gap-4 items-baseline'>
                <LargeHeading size='xs' className='text-white flex flex-row items-center md:gap-1'>
                  {post.recipe_data.avgRating} <Icons.Star size={24} className='scale-75 md:scale-100' fill='white' />
                </LargeHeading>
                <Paragraph className='text-white'>
                  by {post.recipe_data.reviewCount} {post.recipe_data.reviewCount === 1 ? 'user' : 'users'}
                </Paragraph>
              </div>
              <div className='flex flex-col md:flex-row md:gap-6 -mb-2'>
                <Paragraph className='text-white'>
                  {`Cook : ${post.recipe_data.cooktime}`}
                </Paragraph>
                <Paragraph className='text-white'>
                  {`Prep : ${post.recipe_data.preptime}`}
                </Paragraph>
              </div>
              <RecipeActions recipe_id={parseInt(params.id)} />

            </div>
            <Image
              src={post.recipe_data.recipe_image}
              alt='Recipe Image'
              className='md:w-1/2'
              width={500}
              height={500} />
          </div>
          <div className='flex flex-col justify-center gap-6 md:gap-32 md:flex-row bg-slate-100 w-full pt-8 pb-8'>
            <div className='flex flex-col justify-start items-center gap-1'>
              <LargeHeading size='xs'>
                Ingredients
              </LargeHeading>
              <div className='flex flex-row justify-start items-center gap-8'>
                <div className='flex flex-col justify-center items-center'>
                  {post.recipe_data.ingredients.map((ingredient: ingredient) => (
                    <Paragraph key={ingredient.name} className='text-end'>
                      {ingredient.amount}
                    </Paragraph>
                  ))}
                </div>
                <div className='flex flex-col justify-center items-center'>
                  {post.recipe_data.ingredients.map((ingredient: ingredient) => (
                    <Paragraph key={ingredient.name} className='text-start w-full'>
                      {ingredient.name}
                    </Paragraph>
                  ))}
                </div>
              </div>
            </div>
            <div className='flex flex-col justify-start items-center gap-1 px-8'>
              <LargeHeading size='xs'>
                Instructions
              </LargeHeading>
              <Paragraph size='sm' className='text-start'>
                {post.recipe_data.instructions}
              </Paragraph>
            </div>
          </div>
          <div className='flex flex-col items-center justify-center bg-slate-800 gap-8 w-full py-8 px-8'>
            <CommentForm id={params.id} />
            {
              comments.length === 0 ? (
                <Paragraph className='text-white'>
                  No reviews yet
                </Paragraph>
              ) : (
                <div className='flex flex-col items-center justify-start w-full gap-4 pt-4'>
                  {
                    comments.map((comment: any) =>
                      <CommentCard key={comment.review_id} reviewId={comment.review_id} author={comment.username} message={comment.reviewText} rating={comment.rating} />
                    )
                  }
                </div>
              )
            }
          </div>
        </div>
      </div>
    </div>
  )
}

export default Page
