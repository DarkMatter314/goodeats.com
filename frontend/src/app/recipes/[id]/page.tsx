'use client'

import LargeHeading from '@/components/ui/LargeHeading';
import Paragraph from '@/components/ui/Paragraph';
import Image from 'next/image';
import Icons from '@/components/Icons';
import CommentForm from '@/components/CommentForm';
import { RecipeActions } from '@/components/RecipeActions';
// import { useRouter } from 'next/router';

interface ingredient {
  amount: string;
  name: string;
}

// import { usePathname, useRouter, useSearchParams } from 'next/navigation'

async function getRecipe(recipeId: string) {
  const res = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}`);
  return res.json();
}

const Page = async ({ params }) => {
  // const router = useRouter()
  // const id : string = router.query.id || '1'
  // const post = feedRecipes[id?.toNumber()]

  const post = await getRecipe(params.id);

  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container max-w-full mx-auto w-full h-full'>
        <div className='h-full gap-0 flex flex-col justify-start items-center'>
          <div className='flex pt-32 flex-col justify-between items-center gap-8 md:flex-row md:px-10 bg-violet-800 w-full px-8 pb-8'>
            <div className='flex flex-col justify-center items-center'>
              <LargeHeading className='text-white text-center w-full pb-2'>
                {post.name}
              </LargeHeading>
              <LargeHeading size='xs' className='text-white font-bold pb-2'>
                {`${post.username}`}
              </LargeHeading>
              <Paragraph className='text-white flex flex-row items-center pb-1'>
                {`${post.avgRating}  `} <Icons.Star size={16} />
              </Paragraph>
              <Paragraph className='text-white pb-1'>
                {`Cook : ${post.cooktime}`}
              </Paragraph>
              <Paragraph className='text-white pb-1'>
                {`Prep : ${post.preptime}`}
              </Paragraph>
              <RecipeActions />
            </div>
            <Image src={post.recipe_image} alt='Recipe Image' width={500} height={500} />
          </div>
          <div className='flex flex-col justify-center gap-6 md:gap-32 md:flex-row bg-slate-100 w-full pt-8 pb-8'>
            <div className='flex flex-col justify-start items-center gap-1'>
              <LargeHeading size='xs'>
               Ingredients
              </LargeHeading>
              <div className='flex flex-row justify-start items-center gap-8'>
                <div className='flex flex-col justify-center items-center'>
                  {post.ingredients.map((ingredient: ingredient) => (
                    <Paragraph key={ingredient.amount} className='text-end'>
                        {ingredient.amount}
                    </Paragraph>
                  ))}
                </div>
                <div className='flex flex-col justify-center items-center'>
                  {post.ingredients.map((ingredient: ingredient) => (
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
                {post.instructions}
              </Paragraph>
            </div>
          </div>
          <div className='flex flex-col justify-center bg-purple-800 w-full pt-8 pb-8'>
            <CommentForm />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Page
