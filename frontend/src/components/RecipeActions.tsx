import { Icons } from '@/components/Icons'
import { IconButton } from '@/ui/Button'
import AddToCollectionDialog from '@/components/AddToCollectionDialog'
import * as jose from 'jose';




export function RecipeActions({recipe_id}:{recipe_id:number}){

  const token = localStorage.getItem('token');
  let user_id = 0;
  let username = '';
  if (token) {
    user_id = jose.decodeJwt(token as string).user_id as number;
    username = jose.decodeJwt(token as string).user as string;
  }
  if (!username) {
    return null;
  }


  return (
    <div hidden={username ? false : true} className='flex flex-row items-center gap-2 text-white'>
      <IconButton icon={Icons.Heart} variant='ghost' className='hover:bg-purple-700' />
      <AddToCollectionDialog username={username} user_id={user_id} recipe_id={recipe_id}/>
    </div>
  )







}
