import { supabase } from '../lib/supabase.js';

export async function getInterpreterById(languageId){
  try{
    const { data, error} = await supabase
      .from('interpreters')
      .select(`id, first_name, last_name, interpreter_languages!inner(language_id)`)
  .eq('interpreter_languages.language_id', languageId);
    if (error){
      console.error('Error fetching interpreter by ID:', error);
      return[];
    }
    return data;
  } catch (error){
    console.error('An unexpected error occurred:', error.message);
    return [];
  }
}