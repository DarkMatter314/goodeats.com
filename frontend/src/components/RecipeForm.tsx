'use client'

import * as Form from '@radix-ui/react-form';
import { Button } from '@/ui/Button';

const RecipeForm = () => (
  <Form.Root className='max-w-7xl lg:w-[854px] w-10/12 items-center px-8 md:px-0 pb-8'>
    <Form.Field className='grid mb-[6px] md:mb-[10px]' name='username'>
      <div className='flex items-baseline justify-between'>
        <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
          Title
        </Form.Label>
        <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
          Please enter recipe title
        </Form.Message>
      </div>
      <Form.Control asChild>
        <input
        className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
        type='username'
        required
        />
      </Form.Control>
    </Form.Field>
    <div className='flex w-full md:gap-[10px] gap-0 md:flex-row flex-col'>
      <Form.Field className='grid mb-[6px] md:mb-[10px] w-full' name='cookTime'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Cook time
          </Form.Label>
          <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
            Please enter cook time
          </Form.Message>
        </div>
        <Form.Control asChild>
          <input
          className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
          type='email'
          required
          />
        </Form.Control>
      </Form.Field>
      <Form.Field className='grid mb-[6px] md:mb-[10px] w-full' name='prepTime'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Prep time
          </Form.Label>
          <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
            Please enter prep time
          </Form.Message>
        </div>
        <Form.Control asChild>
          <input
          className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
          type='email'
          required
          />
        </Form.Control>
      </Form.Field>
    </div>
    <Form.Field className='grid mb-[6px] md:mb-[10px] w-full' name='description'>
      <div className='flex items-baseline justify-between'>
        <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
          Description
        </Form.Label>
        <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
          Please enter description
        </Form.Message>
      </div>
      <Form.Control asChild>
        <textarea
        className='pt-1 box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[100px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
        required
        />
      </Form.Control>
    </Form.Field>
    <Form.Field className='grid mb-[15px]' name='instructions'>
      <div className='flex items-baseline justify-between'>
        <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
          Instructions
        </Form.Label>
        <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
          Please enter instructions
        </Form.Message>
      </div>
      <Form.Control asChild>
        <textarea
        className='pt-1 box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[100px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
        required
        />
      </Form.Control>
    </Form.Field>
    <div className='flex flex-row w-full justify-center md:justify-end'>
      <Form.Submit asChild>
        <Button className='w-full md:w-1/2'>
          Post
        </Button>
      </Form.Submit>
    </div>
  </Form.Root>
);

export default RecipeForm
