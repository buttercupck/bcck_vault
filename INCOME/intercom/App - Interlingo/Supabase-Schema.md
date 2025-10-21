-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.client_requests (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  commitment_block_id uuid NOT NULL,
  language_id uuid NOT NULL,
  program_id uuid,
  client_name text NOT NULL,
  case_number text,
  meeting_type text NOT NULL,
  requestor_email text,
  specific_location_details text,
  key_contact_name text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  charges text,
  CONSTRAINT client_requests_pkey PRIMARY KEY (id),
  CONSTRAINT fk_commitment_block FOREIGN KEY (commitment_block_id) REFERENCES public.commitment_blocks(id),
  CONSTRAINT fk_language FOREIGN KEY (language_id) REFERENCES public.languages(id),
  CONSTRAINT fk_program FOREIGN KEY (program_id) REFERENCES public.court_programs(id)
);
CREATE TABLE public.commitment_blocks (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  interpreter_id uuid,
  modality text,
  start_time timestamp with time zone,
  end_time timestamp with time zone,
  duration integer DEFAULT (EXTRACT(epoch FROM (end_time - start_time)) / (60)::numeric),
  status text DEFAULT 'Initial'::text,
  created_at timestamp with time zone DEFAULT now(),
  location_id uuid,
  CONSTRAINT commitment_blocks_pkey PRIMARY KEY (id),
  CONSTRAINT requests_interpreter_id_fkey FOREIGN KEY (interpreter_id) REFERENCES public.interpreters(id),
  CONSTRAINT commitment_blocks_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(id)
);
CREATE TABLE public.court_programs (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  description text,
  CONSTRAINT court_programs_pkey PRIMARY KEY (id)
);
CREATE TABLE public.interpreter_aliases (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  alias text NOT NULL,
  interpreter_id uuid,
  CONSTRAINT interpreter_aliases_pkey PRIMARY KEY (id),
  CONSTRAINT interpreter_aliases_interpreter_id_fkey FOREIGN KEY (interpreter_id) REFERENCES public.interpreters(id)
);
CREATE TABLE public.interpreter_languages (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  interpreter_id uuid,
  language_id uuid,
  proficiency_rank integer,
  certification text,
  CONSTRAINT interpreter_languages_pkey PRIMARY KEY (id),
  CONSTRAINT interpreter_languages_interpreter_id_fkey FOREIGN KEY (interpreter_id) REFERENCES public.interpreters(id),
  CONSTRAINT interpreter_languages_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.languages(id)
);
CREATE TABLE public.interpreters (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  first_name text NOT NULL,
  last_name text NOT NULL,
  license_number text,
  phone text,
  email text,
  city text,
  state text,
  timezone text,
  rate text,
  internal_notes text,
  is_agency boolean DEFAULT false,
  agency_name text,
  agency_contact_email text,
  agency_contact_phone text,
  modality_preferences ARRAY,
  is_local boolean DEFAULT false,
  CONSTRAINT interpreters_pkey PRIMARY KEY (id)
);
CREATE TABLE public.langchain_pg_collection (
  name character varying,
  cmetadata json,
  uuid uuid NOT NULL,
  CONSTRAINT langchain_pg_collection_pkey PRIMARY KEY (uuid)
);
CREATE TABLE public.langchain_pg_embedding (
  collection_id uuid,
  embedding USER-DEFINED,
  document character varying,
  cmetadata json,
  custom_id character varying,
  uuid uuid NOT NULL,
  CONSTRAINT langchain_pg_embedding_pkey PRIMARY KEY (uuid),
  CONSTRAINT langchain_pg_embedding_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES public.langchain_pg_collection(uuid)
);
CREATE TABLE public.languages (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  CONSTRAINT languages_pkey PRIMARY KEY (id)
);
CREATE TABLE public.locations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  org_id uuid,
  zoom_link text,
  zoom_login text,
  type text DEFAULT 'courtroom'::text CHECK (type = ANY (ARRAY['courtroom'::text, 'law_office'::text])),
  address text,
  notes text,
  CONSTRAINT locations_pkey PRIMARY KEY (id),
  CONSTRAINT locations_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id)
);
CREATE TABLE public.obsidian_knowledge_vectors (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  embedding USER-DEFINED,
  document text,
  cmetadata jsonb,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT obsidian_knowledge_vectors_pkey PRIMARY KEY (id)
);
CREATE TABLE public.organizations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  abbreviation text UNIQUE,
  address text,
  type text,
  street text,
  city text,
  state text,
  zip text,
  CONSTRAINT organizations_pkey PRIMARY KEY (id)
);