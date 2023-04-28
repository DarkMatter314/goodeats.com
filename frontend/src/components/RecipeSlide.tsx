import Image from 'next/image'
import Link from 'next/link'
import LargeHeading from '@/ui/LargeHeading'
import type {RecipeCardProps} from '@/components/RecipeCard'
import Icons from '@/components/Icons'

interface scrollAreaProps
{
  feedRecipes: Array<any>
  header: string
}

export function ScrollArea({feedRecipes, header}:scrollAreaProps) {
  // let feedRecipes = await getAllRecipes();
  return (
    <div className='items-center justify-center flex flex-col gap-6 lg:h-[900px] md:h-[700px] h-[600px] bg-slate-100'>
      <LargeHeading className='font-sans font-medium'>
        {header}
      </LargeHeading>
      <div className='w-full snap-x sm:snap-none md:px-8 px-4 lg:h-[600px] md:h-[400px] h-96 justify-start items-center inset-x-20 grid grid-rows-1 grid-flow-col gap-8 overflow-y-clip overflow-x-scroll 2xl:max-w-screen-2xl xl:max-w-screen-xl lg:max-w-screen-lg md:max-w-screen-md sm:max-w-screen-sm max-w-xs'>
        {feedRecipes.length > 0 && feedRecipes.map((post) => {
          return (
            <RecipeBox key={post.recipe?.recipe_id} recipeName={post.recipe?.name} recipeAuthor={post.user?.name} recipeId={post.recipe?.recipe_id}
              recipeImage={post.recipe?.recipe_image} recipeDescription={post.recipe?.description} recipeRating={post.recipe?.avgRating} recipeReviewCount={post.recipe?.reviewCount} />
          )
        })
        }
      </div>
    </div>
  )
}


export function RecipeBox({ recipeName, recipeAuthor, recipeImage, recipeDescription, recipeId, recipeRating }: RecipeCardProps) {
  return (
    <Link className='snap-center flex flex-col justify-center  items-center md:gap-10 gap-16  lg:w-72 w-44 max-w-7xl rounded-lg hover:scale-110 hover:shadow-lg hover:shadow-orange-100 transition-transform hover:overflow-visible'
      href={`/recipes/${recipeId}`}>
      <Image src={recipeImage} alt={recipeName} width={300} height={500} className='rounded-lg lg:h-80 lg:w-72  object-cover sm:h-40 sm:w-36' />
      <LargeHeading className='text-center flex-wrap max-w-xs max-h-5 gap-5 sm:text-sm font-medium' size='xxs'>
        {recipeName?.slice(0, 30) + (recipeName?.length > 30 ? '...' : '')}
      </LargeHeading>
      <div className='text-center font-semibold flex flex-row items-center'>
        {recipeRating} <Icons.Star size={16} fill='black' />
      </div>
    </Link>
  )
}
