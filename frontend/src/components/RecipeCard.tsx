'use client'

import Image from 'next/image'
import LargeHeading from '@/ui/LargeHeading'
import Paragraph from '@/ui/Paragraph'

interface RecipeCardProps {
  recipeName: string
  recipeDescription: string
  recipeAuthor: string
  recipeId: number
  recipeImage: string
}

export function RecipeCard({recipeName, recipeAuthor, recipeImage, recipeDescription, recipeId}: RecipeCardProps) {
  return (
    <div key={recipeId} className='flex flex-col md:flex-row gap-4 w-full max-w-7xl'>
      <Image src={recipeImage} alt={recipeName} width={200} height={200} className='rounded-lg' />
      <div className='flex flex-col'>
        <div className='flex flex-row w-full justify-between pb-1'>
          <LargeHeading className='text-start' size='xs'>
            {recipeName}
          </LargeHeading>
        </div>
        <Paragraph className='text-start font-bold'>
          {recipeAuthor}
        </Paragraph>
        <Paragraph size='sm' className='w-full text-start'>
          {recipeDescription}
        </Paragraph>
      </div>
    </div>
  )
}
