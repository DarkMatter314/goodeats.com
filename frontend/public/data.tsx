interface ingredient {
  quantity: number;
  name: string;
}

export interface Recipe {
  id: number;
  name: string;
  ingredients: Array<ingredient>;
  instructions: string;
  username: string;
  rating: number;
  recipe_image: string;
  description: string;
  cooktime: string;
  preptime: string;
  reviewcount: number;
}

export const feedRecipes: Array<Recipe> = [
  {
    id: 1,
    name: 'Chicken Parmesan',
    instructions: 'Cook the chicken, cook the pasta, mix it all together',
    ingredients: [
      {
        quantity: 1,
        name: 'Chicken'
      },
      {
        quantity: 2,
        name: 'Parmesan'
      },
      {
        quantity: 3,
        name: 'Pasta'
      }
    ],
    username: 'john_doe',
    rating: 4.5,
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    id: 2,
    name: 'Moustalevria (Grape Wine Pudding)',
    instructions: 'Cook the chicken, cook the pasta, mix it all together',
    ingredients: [
      {
        quantity: 1,
        name: 'Chicken'
      },
      {
        quantity: 2,
        name: 'Parmesan'
      },
      {
        quantity: 3,
        name: 'Pasta'
      }
    ],
    username: 'John Doe',
    rating: 4.5,
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    id: 3,
    name: 'Chicken Parmesan',
    instructions: 'Cook the chicken, cook the pasta, mix it all together',
    ingredients: [
      {
        quantity: 1,
        name: 'Chicken'
      },
      {
        quantity: 2,
        name: 'Parmesan'
      },
      {
        quantity: 3,
        name: 'Pasta'
      }
    ],
    username: 'John Doe',
    rating: 4.5,
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    id: 4,
    name: 'Chicken Parmesan',
    instructions: 'Cook the chicken, cook the pasta, mix it all together',
    ingredients: [
      {
        quantity: 1,
        name: 'Chicken'
      },
      {
        quantity: 2,
        name: 'Parmesan'
      },
      {
        quantity: 3,
        name: 'Pasta'
      }
    ],
    username: 'John Doe',
    rating: 4.5,
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    id: 5,
    name: 'Chicken Parmesan',
    instructions: 'Cook the chicken, cook the pasta, mix it all together',
    ingredients: [
      {
        quantity: 1,
        name: 'Chicken'
      },
      {
        quantity: 2,
        name: 'Parmesan'
      },
      {
        quantity: 3,
        name: 'Pasta'
      }
    ],
    username: 'John Doe',
    rating: 4.5,
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    id: 6,
    name: 'Chicken Parmesan',
    instructions: 'Cook the chicken, cook the pasta, mix it all together',
    ingredients: [
      {
        quantity: 1,
        name: 'Chicken'
      },
      {
        quantity: 2,
        name: 'Parmesan'
      },
      {
        quantity: 3,
        name: 'Pasta'
      }
    ],
    username: 'John Doe',
    rating: 4.5,
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
];

interface Collection {
  collectionId: number;
  name: string;
  username: string;
  recipe_image: string;
  description: string;
  recipeList: Array<Recipe>;
}

export const feedCollections: Array<Collection> = [
  {
    collectionId: 1,
    name: 'non veg',
    username: 'john_doe',
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection, A delicious chicken parmesan collection, A delicious chicken parmesan collection, A delicious chicken parmesan collection, ',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 2,
    name: 'non veg',
    username: 'john_doe',
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 3,
    name: 'non veg',
    username: 'john_doe',
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 4,
    name: 'non veg',
    username: 'john_doe',
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 5,
    name: 'non veg',
    username: 'john_doe',
    recipe_image: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
]
