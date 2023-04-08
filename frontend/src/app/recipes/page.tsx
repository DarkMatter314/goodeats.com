import LargeHeading from '@/components/ui/LargeHeading';
import React from 'react';
import { Metadata } from 'next'
import SearchBar from '@/components/SearchBar';
import { RecipeCard } from '@/components/RecipeCard';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Goodeats | Browse Recipes',
}

interface RecipeCardProps {
  name: string
  description: string
  username: string
  id: number
  recipe_image: string
}

async function getAllRecipes() {
  const res = await fetch('http://127.0.0.1:5000/');
  return res.json();
}

export default async function page() {
  let feedRecipes = await getAllRecipes();
  feedRecipes = feedRecipes.slice(0, 10);

  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='h-full gap-8 flex flex-col justify-start items-center'>
          <div className='flex flex-col items-center gap-6'>
            <LargeHeading>
              Browse all Recipes
            </LargeHeading>
            <SearchBar />
          </div>
          <div className='h-full flex flex-col justify-start place-items-start px-8'>
            {feedRecipes.map((recipe: RecipeCardProps) => (
              <Link href={`/recipes/${recipe.id}`} key={recipe.id} className='mb-8'>
                <RecipeCard recipeId={recipe.id} recipeName={recipe.name} recipeImage={recipe.recipe_image} recipeAuthor={recipe.username} recipeDescription={recipe.description} />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
