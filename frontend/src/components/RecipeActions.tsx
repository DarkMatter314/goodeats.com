import { Icons } from '@/components/Icons'
import { IconButton } from '@/components/ui/Button'
import AddToCollectionDialog from './AddToCollectionDialog'

export function RecipeActions() {
  return (
    <div className='flex flex-row items-center gap-2 text-white'>
      <IconButton icon={Icons.Heart} variant='ghost' className='hover:bg-purple-700' />
      <AddToCollectionDialog />
    </div>
  )
}
