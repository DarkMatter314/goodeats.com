'use client'

import { useRouter } from 'next/navigation';
import * as Form from '@radix-ui/react-form';
import * as jose from 'jose';
import { Button } from '@/ui/Button';
import { toast } from '@/ui/toast';
import { useState } from 'react';

const RecipeForm = () => {

  const router = useRouter();
  const [imageSrc, setImageSrc] = useState<string>('');

  async function handleImageChange (event: any) {
    event.preventDefault();

    const form = event.currentTarget;
    let fileInput = null as any;

    for (const ele of form.elements) {
      if (ele.name === 'file') {
        fileInput = ele;
        break;
      }
    }

    const formData = new FormData();

    for ( const file of fileInput.files ) {
      formData.append('file', file);
    }

    formData.append('upload_preset', 'goodeats');

    const data = await fetch(`https://api.cloudinary.com/v1_1/${process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME}/image/upload`, {
      method: 'POST',
      body: formData
    }).then(r => r.json());

    setImageSrc(data.secure_url);
  }

  async function submitForm(data) {
    const token = localStorage.getItem('token');

    // check if logged in
    if (!token) {
      toast({
        title: 'Error',
        message: 'Please login to create a recipe',
        type: 'error',
        duration: 2000,
      });
      return;
    }

    // parse ingredients
    let ingredients : Array<any> = [];
    data.ingredients = data.ingredients.split('\n');
    for (let i = 0; i < data.ingredients.length; i++) {
      if (data.ingredients[i].trim() === '') continue;
      const ingredient = data.ingredients[i].split(' ');
      if (ingredient.length < 2 || ingredient[0].trim() === '' || ingredient.slice(1).join(' ').trim() === '') {
        toast({
          title: 'Error',
          message: 'Please enter ingredients in the format: "Quantity <space> Ingredient Name"',
          type: 'error',
          duration: 2000,
        });
        return;
      }
      ingredients.push([ingredient.slice(1).join(' ').trim(), ingredient[0]]);
    }
    data.ingredients = ingredients;

    // assign user_id
    data.user_id = parseInt(jose.decodeJwt(token).user_id as string);

    // parse keywords
    data.keywords = data.keywords.split(',').map((keyword: string) => keyword.trim());

    // set image
    if (imageSrc) {
      data.recipe_image = imageSrc;
    }

    const response = await fetch('/api/recipe/post', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const json = await response.json();
    if (json.recipe_data) {
      toast({
        title: 'Success',
        message: 'Recipe created',
        type: 'success',
        duration: 1500,
      })
      setTimeout(() => {
        router.push('/recipes');
      }, 1000);
    }
    else {
      const error_msg = json.name
      || json.instructions
      || json.description
      || json.ingredients
      || json.cooktime
      || json.preptime;
      toast({
        title: 'Error',
        message: error_msg,
        type: 'error',
        duration: 2000,
      });
    }
  };

  return (
    <Form.Root className='max-w-7xl lg:w-[854px] w-10/12 items-center px-8 md:px-0 pb-8'
      onSubmit={(event) => {
        const data = Object.fromEntries(new FormData(event.currentTarget));
        submitForm(data);
        event.preventDefault();
      }}
    >
      <Form.Field className='grid mb-[6px] md:mb-[10px]' name='name'>
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
            type='name'
            required
          />
        </Form.Control>
      </Form.Field>
      <div className='flex w-full md:gap-[10px] gap-0 md:flex-row flex-col'>
        <Form.Field className='grid mb-[6px] md:mb-[10px] w-full' name='cooktime'>
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
              type='text'
              required
            />
          </Form.Control>
        </Form.Field>
        <Form.Field className='grid mb-[6px] md:mb-[10px] w-full' name='preptime'>
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
              type='text'
              required
            />
          </Form.Control>
        </Form.Field>
      </div>
      <div className='flex w-full md:gap-[10px] gap-0 md:flex-row flex-col'>
        <Form.Field className='grid mb-[6px] md:mb-[10px] w-full' name='keywords'>
          <div className='flex items-baseline justify-between'>
            <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
              Keywords
            </Form.Label>
            <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
              Please enter keywords
            </Form.Message>
          </div>
          <Form.Control asChild>
            <input
              className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
              type='text'
              required
            />
          </Form.Control>
        </Form.Field>
        <Form.Field className='grid mb-[6px] md:mb-[10px] w-full' name='recipeServings'>
          <div className='flex items-baseline justify-between'>
            <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
              No. of Servings
            </Form.Label>
            <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
              Please enter number of servings
            </Form.Message>
          </div>
          <Form.Control asChild>
            <input
              className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
              type='text'
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
            className='pt-1 box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[100px] appearance-none items-center justify-center rounded-[4px] px-[10px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
            required
          />
        </Form.Control>
      </Form.Field>
      <Form.Field className='grid mb-[6px] md:mb-[10px]' name='ingredients'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Ingredients
          </Form.Label>
          <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
            Please enter ingredients
          </Form.Message>
        </div>
        <Form.Control asChild>
          <textarea
            className='pt-1 box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[100px] appearance-none items-center justify-center rounded-[4px] px-[10px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
            required
          />
        </Form.Control>
      </Form.Field>
      <Form.Field className='grid mb-[6px] md:mb-[10px]' name='instructions'>
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
            className='pt-1 box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[100px] appearance-none items-center justify-center rounded-[4px] px-[10px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
            required
          />
        </Form.Control>
      </Form.Field>
      <form className='grid mb-[15px]' onChange={handleImageChange}>
        <p className='text-black font-medium text-[15px] leading-[35px]'>
          Upload Image
        </p>
        <input type='file' accept='image/\*' name='file'/>
      </form>
      <div className='flex flex-row w-full justify-center md:justify-end'>
        <Form.Submit asChild>
          <Button className='w-full md:w-1/2'>
            Post
          </Button>
        </Form.Submit>
      </div>
    </Form.Root>
  )
};

export default RecipeForm
