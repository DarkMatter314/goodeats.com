interface ingredient {
  quantity: number;
  name: string;
}

interface Recipe {
  recipeId: number;
  name: string;
  ingredients: Array<ingredient>;
  instructions: string;
  username: string;
  rating: number;
  imageUrl: string;
  description: string;
  datepublished: Date;
  cooktime: string;
  preptime: string;
  reviewcount: number;
}

export const feedRecipes: Array<Recipe> = [
  {
    recipeId: 1,
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
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    datepublished: new Date(2023, 3, 1),
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    recipeId: 2,
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
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    datepublished: new Date(2023, 3, 1),
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    recipeId: 3,
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
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    datepublished: new Date(2023, 3, 1),
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    recipeId: 4,
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
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    datepublished: new Date(2023, 3, 1),
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    recipeId: 5,
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
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    datepublished: new Date(2023, 3, 1),
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
  {
    recipeId: 6,
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
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan recipe',
    datepublished: new Date(2023, 3, 1),
    cooktime: '30 minutes',
    preptime: '10 minutes',
    reviewcount: 10
  },
];

interface Collection {
  collectionId: number;
  name: string;
  username: string;
  imageUrl: string;
  description: string;
  recipeList: Array<Recipe>;
}

export const feedCollections: Array<Collection> = [
  {
    collectionId: 1,
    name: 'non veg',
    username: 'john_doe',
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection, A delicious chicken parmesan collection, A delicious chicken parmesan collection, A delicious chicken parmesan collection, ',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 2,
    name: 'non veg',
    username: 'john_doe',
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 3,
    name: 'non veg',
    username: 'john_doe',
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 4,
    name: 'non veg',
    username: 'john_doe',
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
  {
    collectionId: 5,
    name: 'non veg',
    username: 'john_doe',
    imageUrl: 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
    description: 'A delicious chicken parmesan collection',
    recipeList: [feedRecipes[0], feedRecipes[1], feedRecipes[2]]
  },
]
