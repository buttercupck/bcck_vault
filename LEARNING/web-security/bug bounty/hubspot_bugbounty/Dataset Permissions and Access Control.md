`// **IMPORTANT**
//
// When making any changes to access/permissions, be sure to refer to "Updating
// permissions/access checklist" to ensure that all dependencies behave as expected
// https://docs.google.com/document/d/1rviBNncodOgFDSwjV_yZ6nejiJkhzZvzsBZeehL9bWg

// dataset builder scopes
const DATASETS_ADMIN_SCOPE = 'datasets-super-admin';
const SUPER_ADMIN_SCOPE = 'super-admin';
const GLOBAL_DATASETS_ACCESS_SCOPE = 'reporting-global-datasets-access';
const CUSTOM_DATASETS_ACCESS_SCOPE = 'reporting-datasets-access';
const REPORTING_DATASETS_READ_SCOPE = 'reporting-datasets-read';
const REPORTING_DATASETS_WRITE_SCOPE = 'reporting-datasets-write';
export const getDatasetsLimits = userInfo => {
  return {
    customDatasetLimit: userInfo.portal.limits['reporting-datasets-limit'] || 0,
    propertyFieldLimit: userInfo.portal.limits['reporting-datasets-properties-limit'] || 0,
    derivedFieldLimit: userInfo.portal.limits['reporting-datasets-derived-fields-limit'] || 0
  };
};
const getIsAdmin = scopes => {
  return scopes.includes(DATASETS_ADMIN_SCOPE) || scopes.includes(SUPER_ADMIN_SCOPE);
};
**export function getDatasetAccessLevels**({
  userInfo: {
    user: {
      scopes
    }
  }
}) {
  const datasetsAdmin = getIsAdmin(scopes);
  if (!scopes.includes(GLOBAL_DATASETS_ACCESS_SCOPE)) {
    return {
      appAccess: false,
      customDatasetsAccess: false,
      readAccess: false,
      writeAccess: false,
      datasetsAdmin
    };
  }
  const customDatasetsAccess = scopes.includes(CUSTOM_DATASETS_ACCESS_SCOPE);

  // Permissions are hierarchical: Users with the read **scope** have read __only__
  // access
  //
  // When a user is granted the writer **role**, the write **scope** check
  // guarantees that the user has read access, however their scopes array
  // from userInfo will not include the read **scope**
  if (scopes.includes(REPORTING_DATASETS_WRITE_SCOPE)) {
    return {
      appAccess: true,
      customDatasetsAccess,
      readAccess: true,
      writeAccess: true,
      datasetsAdmin
    };
  }
  if (scopes.includes(REPORTING_DATASETS_READ_SCOPE)) {
    return {
      appAccess: true,
      customDatasetsAccess,
      readAccess: true,
      writeAccess: false,
      datasetsAdmin
    };
  }

  // Portal has datasets access, but user has not been granted any dataset roles.
  return {
    appAccess: true,
    customDatasetsAccess,
    readAccess: false,
    writeAccess: false,
    datasetsAdmin
  };
}
**export const getUserCanModifyDataset** = ({
  userInfo,
  ownerId
}) => {
  const accessLevel = getDatasetAccessLevels({
    userInfo
  });
  if (!accessLevel.writeAccess) {
    return false;
  }
  if (getIsAdmin(userInfo.user.scopes)) {
    return true;
  }
  return userInfo.user.user_id === ownerId;
};`