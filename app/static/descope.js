const projectId = "P2iRuQ0iD6pJVWtofatuMIdl1Xsj"
const sdk = Descope({ projectId: projectId, persistTokens: true, autoRefresh: true })
const sessionToken = sdk.getSessionToken()